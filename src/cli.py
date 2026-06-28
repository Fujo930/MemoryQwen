"""
MemoryQwen CLI — 本地命令行工具
用法:
  python -m src.cli health
  python -m src.cli ingest <path>
  python -m src.cli chat "<message>" [--session SESSION] [--model-tier light|deep]
  python -m src.cli correct --wrong "..." --correct "..." [--session SESSION] [--failure-type TYPE]
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from src.config import load_config
from src.model_client import create_model_client
from src.memory_store import create_memory_store
from src.retrieval.keyword import KeywordRetriever
from src.agent.chat_service import AgentChatService
from src.agent.error_learning import ErrorLearningService
from src.agent.strategy_learning import StrategyLearningService
from src.agent.models import ChatRequest, CorrectionRequest
from src.ingestion.pipeline import IngestionPipeline
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memoryqwen",
        description="MemoryQwen 本地 AI Agent 命令行工具",
    )
    parser.add_argument("--config", default="config/default.yaml", help="配置文件路径")

    sub = parser.add_subparsers(dest="command", required=True)

    # health
    sub.add_parser("health", help="检查系统状态")

    # ingest
    ingest = sub.add_parser("ingest", help="导入文件/目录")
    ingest.add_argument("path", help="文件或目录路径")
    ingest.add_argument("--recursive", action="store_true", default=True, help="递归导入子目录")

    # chat
    chat = sub.add_parser("chat", help="发送聊天消息")
    chat.add_argument("message", help="消息内容")
    chat.add_argument("--session", default="default", help="会话 ID")
    chat.add_argument("--model-tier", default="light", choices=["light", "deep"], help="模型层级")
    chat.add_argument("--debug-memory", action="store_true", help="显示记忆检索详情")
    chat.add_argument("--web", action="store_true", dest="use_web", help="允许本次聊天使用临时网页查询")
    chat.add_argument("--deep", action="store_true", dest="use_deep", help="使用 deep mode (14B)")

    # memory
    memory = sub.add_parser("memory", help="记忆存储管理")
    mem_sub = memory.add_subparsers(dest="memory_cmd", required=True)
    mem_sub.add_parser("stats", help="显示各 store 计数")

    # correct
    correct = sub.add_parser("correct", help="提交纠错")
    correct.add_argument("--session", default="default", help="会话 ID")
    correct.add_argument("--wrong", required=True, help="错误回答")
    correct.add_argument("--correct", required=True, help="正确回答")
    correct.add_argument("--failure-type", default="general", help="错误类型")
    correct.add_argument("--strategy", default="", help="修正策略（可选）")

    # profile
    profile = sub.add_parser("profile", help="模型 profile 管理")
    prof_sub = profile.add_subparsers(dest="profile_cmd", required=True)
    prof_sub.add_parser("show", help="显示当前 profile")
    prof_validate = prof_sub.add_parser("validate", help="校验 profile 文件")
    prof_validate.add_argument("path", help="profile 文件路径")
    prof_eval = prof_sub.add_parser("eval", help="运行模型能力评估")
    prof_eval.add_argument("--model-id", required=True, help="模型 ID")
    prof_eval.add_argument("--output", default="", help="保存 profile 的路径")
    prof_eval.add_argument("--dry-run", action="store_true", help="只打印评估用例，不调用模型")

    # guardian
    guardian = sub.add_parser("guardian", help="GPU Guardian 状态")
    guard_sub = guardian.add_subparsers(dest="guardian_cmd", required=True)
    guard_sub.add_parser("status", help="显示 GPU 让路状态")
    guard_sub.add_parser("json", help="输出 JSON 格式 GPU 状态")

    # job / task
    job = sub.add_parser("job", help="后台任务管理")
    job_sub = job.add_subparsers(dest="job_cmd", required=True)
    jin = job_sub.add_parser("ingest", help="创建 ingestion 任务")
    jin.add_argument("path", help="目录路径")
    jin.add_argument("--guardian", action="store_true", help="启用 guardian checkpoint")

    task = sub.add_parser("task", help="任务管理")
    task_sub = task.add_subparsers(dest="task_cmd", required=True)
    task_sub.add_parser("list", help="列出任务")
    tstat = task_sub.add_parser("status", help="查看任务详情")
    tstat.add_argument("task_id", help="任务 ID")
    tpause = task_sub.add_parser("pause", help="暂停任务")
    tpause.add_argument("task_id", help="任务 ID")
    tpause.add_argument("--reason", default="user_pause", help="暂停原因")
    tresume = task_sub.add_parser("resume", help="恢复任务")
    tresume.add_argument("task_id", help="任务 ID")
    tcancel = task_sub.add_parser("cancel", help="取消任务")
    tcancel.add_argument("task_id", help="任务 ID")

    # web (v0.1.5)
    web = sub.add_parser("web", help="网页查询 (v0.1.5 Internet Query)")
    web_sub = web.add_subparsers(dest="web_cmd", required=True)
    web_search = web_sub.add_parser("search", help="搜索网页")
    web_search.add_argument("query", help="搜索关键词")
    web_search.add_argument("--max-results", type=int, default=5, help="最大结果数")
    web_fetch = web_sub.add_parser("fetch", help="抓取网页")
    web_fetch.add_argument("url", help="网页 URL")
    web_ask = web_sub.add_parser("ask", help="搜索+抓取并回答")
    web_ask.add_argument("question", help="问题")
    web_ask.add_argument("--max-results", type=int, default=3, help="最大抓取数")
    web_ingest = web_sub.add_parser("ingest", help="抓取并存入知识库")
    web_ingest.add_argument("url", help="网页 URL")

    # eval
    ev = sub.add_parser("eval", help="验证评测")
    ev_sub = ev.add_subparsers(dest="eval_cmd", required=False)
    ev_run = ev_sub.add_parser("run", help="运行评测")
    ev_run.add_argument("path", help="题库路径（文件或目录）")
    ev_run.add_argument("--max-questions", type=int, default=0, help="最大题目数")
    ev_run.add_argument("--topic", default="", help="按 topic 过滤")
    ev_run.add_argument("--shuffle", action="store_true", help="打乱顺序")
    ev_run.add_argument("--output-dir", default="training_logs/eval_runs", help="报告输出目录")
    ev_report = ev_sub.add_parser("report", help="查看评测报告")
    ev_report.add_argument("run_id", help="Run ID")
    ev_report.add_argument("--output-dir", default="training_logs/eval_runs", help="报告目录")
    ev_mark = ev_sub.add_parser("mark", help="人工标注结果")
    ev_mark.add_argument("run_id", help="Run ID")
    ev_mark.add_argument("question_id", help="问题 ID")
    ev_mark.add_argument("--correctness", choices=["correct","partial","wrong","unjudged"], default="unjudged")
    ev_mark.add_argument("--failure-type", default="", help="错误类型")
    ev_mark.add_argument("--notes", default="", help="备注")
    ev_mark.add_argument("--output-dir", default="training_logs/eval_runs", help="报告目录")
    ev_export = ev_sub.add_parser("export-corrections", help="导出纠错草稿")
    ev_export.add_argument("run_id", help="Run ID")
    ev_export.add_argument("--output", default="", help="输出文件路径")
    ev_export.add_argument("--format", choices=["markdown","bash"], default="markdown")
    ev_export.add_argument("--include-partial", action="store_true")
    ev_export.add_argument("--failure-type-default", default="hallucination")
    ev_export.add_argument("--output-dir", default="training_logs/eval_runs", help="报告目录")
    ev_judge = ev_sub.add_parser("judge", help="运行 auto-judge")
    ev_judge.add_argument("run_id", help="Run ID")
    ev_judge.add_argument("--mode", choices=["heuristic","llm"], default="heuristic")
    ev_judge.add_argument("--model-id", default="", help="LLM judge model")
    ev_judge.add_argument("--overwrite", action="store_true", help="覆盖已有 manual mark")
    ev_judge.add_argument("--output-dir", default="training_logs/eval_runs", help="报告目录")

    return parser


async def cmd_health(config, store, model_client):
    """检查系统状态"""
    print("MemoryQwen Health Check")
    print("=" * 40)

    # Config
    print(f"✓ Config: {config.system.name} v{config.system.version}")
    print(f"  Data dir: {config.system.data_dir}")
    print(f"  Model: {config.model.default_light_model} / {config.model.default_deep_model}")

    # Memory Store
    try:
        count = await store.count("knowledge_store")
        print(f"✓ Memory Store: OK ({count} knowledge chunks)")
    except Exception as e:
        print(f"✗ Memory Store: {e}")

    # Model Client
    try:
        ok = await model_client.health_check()
        if ok:
            print("✓ Model Client: OK")
        else:
            print("✗ Model Client: Unavailable (health check failed)")
    except Exception as e:
        print(f"✗ Model Client: {e}")

    print("=" * 40)


async def cmd_ingest(config, store, args):
    """导入文件"""
    path = args.path
    print(f"Ingesting: {path}")

    parser = DocumentParser()
    chunker = DocumentChunker()
    pipeline = IngestionPipeline(config, store, parser, chunker)

    p = Path(path)
    if p.is_file():
        result = await pipeline.ingest_file(str(p))
    elif p.is_dir():
        result = await pipeline.ingest_directory(str(p), recursive=args.recursive)
    else:
        print(f"Error: path not found: {path}")
        return

    print(f"  Files seen:    {result.files_seen}")
    print(f"  Files ingested:{result.files_ingested}")
    print(f"  Files skipped: {result.files_skipped}")
    print(f"  Chunks created:{result.chunks_created}")
    print(f"  Chunks stored: {result.chunks_stored}")
    print(f"  Duplicates:    {result.duplicates_skipped}")
    if result.errors:
        print(f"  Errors:        {len(result.errors)}")
        for e in result.errors[:5]:
            print(f"    - {e['file']}: {e['error']}")

    archived = result.metadata.get("archived_sources", 0)
    if archived > 0:
        archive_dir = getattr(config.ingestion, "source_archive_dir", "memory/sources")
        print(f"  Archived:      {archived} → {archive_dir}")


async def cmd_chat(config, store, model_client, args):
    """聊天"""
    debug = getattr(args, 'debug_memory', False)

    retriever = KeywordRetriever(config, store, store_types=["knowledge_store", "error_store", "strategy_store"])
    agent = AgentChatService(config, model_client, retriever, store)

    if debug:
        print(f"Query: {args.message}")
        print(f"Top K: {config.agent.default_top_k}")
        print(f"use_error_memory: {config.agent.use_error_memory}")
        print(f"use_strategy_memory: {config.agent.use_strategy_memory}")
        print("-" * 40)

    request = ChatRequest(session_id=args.session, message=args.message, use_web=getattr(args, "use_web", False), use_deep=getattr(args, "use_deep", False))
    response = await agent.chat(request)

    if debug:
        print(response.answer)
        print("-" * 40)
    else:
        print(response.answer)

    if debug:
        print(f"\nSources ({len(response.sources)}):")
        if response.sources:
            for s in response.sources[:3]:
                print(f"  [S] {s.source_path} ({s.title}) — score {s.score:.2f}")
        else:
            print("  none")

        print(f"\nError References ({len(response.error_sources)}):")
        if response.error_sources:
            for e in response.error_sources[:3]:
                print(f"  [E] {e.task[:60]} — {e.failure_type or 'general'} (score {e.score:.2f})")
        else:
            print("  none")

        print(f"\nStrategy References ({len(response.strategy_sources)}):")
        if response.strategy_sources:
            for s in response.strategy_sources[:3]:
                print(f"  [T] {s.strategy[:80]} — {s.failure_type} (score {s.score:.2f})")
        else:
            print("  none")

        print(f"\nModel: {response.model}")
        print(f"Tokens: {response.prompt_tokens_estimate}")
        print(f"Memory: {', '.join(response.memory_used) if response.memory_used else 'none'}")

        print(f"\nRetrieval count: {response.metadata.get('retrieval_count', 0)}")
        print(f"Error count:     {response.metadata.get('error_count', 0)}")
        print(f"Strategy count:  {response.metadata.get('strategy_count', 0)}")
        ms = response.memory_used
        print(f"\nPrompt sections:")
        print(f"  local_sources:    {'yes' if 'knowledge_store' in ms else 'no'}")
        print(f"  error_memory:     {'yes' if 'error_store' in ms else 'no'}")
        print(f"  strategy_memory:  {'yes' if 'strategy_store' in ms else 'no'}")
        print(f"  recent_chat:      {'yes' if response.metadata.get('recent_messages_count', 0) > 0 else 'no'}")

        if response.metadata.get("capability_guard_triggered"):
            print(f"\nCapability Guard:")
            print(f"  triggered:    yes")
            print(f"  risk_level:   {response.metadata.get('capability_guard_risk_level', 'low')}")
            print(f"  matched_terms: {', '.join(response.metadata.get('capability_guard_terms', []))}")

        print(f"\nRetrieval Gate:")
        print(f"  enabled:       {'yes' if response.metadata.get('retrieval_gate_enabled') else 'no'}")
        print(f"  should_retrieve: {'yes' if response.metadata.get('retrieval_gate_should_retrieve') else 'no'}")
        print(f"  stores:        {', '.join(response.metadata.get('retrieval_gate_stores', []))}")
        print(f"  reason:        {response.metadata.get('retrieval_gate_reason', '')}")
        print(f"  confidence:    {response.metadata.get('retrieval_gate_confidence', 0)}")
        print(f"  risk_level:    {response.metadata.get('retrieval_gate_risk_level', 'low')}")
        print(f"  skipped:       {'yes' if response.metadata.get('retrieval_skipped') else 'no'}")


async def cmd_correct(config, store, args):
    """纠错"""
    els = ErrorLearningService(config, store)

    request = CorrectionRequest(
        session_id=args.session,
        wrong_answer=args.wrong,
        correct_answer=args.correct,
        failure_type=args.failure_type,
        strategy=args.strategy,
    )

    try:
        response = await els.record_correction(request)
        print(f"Correction recorded: {response.saved}")
        print(f"  Error ID:     {response.error_id}")
        print(f"  Failure Type: {response.failure_type}")
        print(f"  Strategy:     {response.strategy[:100] if response.strategy else 'none'}")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Strategy learning
    sl_enabled = getattr(config.agent, "enable_strategy_learning", False)
    print(f"  Strategy learning enabled: {sl_enabled}")

    strategy_generated = False
    strategy_id = "None"
    strategy_warning = None

    if sl_enabled and response.saved:
        # Use the strategy generated by ErrorLearningService (may have default)
        if not request.strategy.strip() and response.strategy:
            request.strategy = response.strategy
        try:
            from src.agent.strategy_learning import StrategyLearningService
            sls = StrategyLearningService(config, store)
            result = await sls.upsert_strategy_from_correction(request, response.error_id)
            if result.get("created"):
                strategy_generated = True
                strategy_id = result.get("strategy_id", "?")[:12] + "..."
                print(f"  Strategy generated: true")
                print(f"  Strategy ID:        {strategy_id}")
            elif result.get("updated"):
                strategy_generated = True
                strategy_id = result.get("strategy_id", "?")[:12] + "..."
                print(f"  Strategy updated (count={result.get('updated_count', 0)})")
                print(f"  Strategy ID:        {strategy_id}")
            else:
                strategy_warning = f"Unexpected result: {result}"
        except Exception as e:
            strategy_warning = f"Strategy learning failed: {e}"
    elif not sl_enabled:
        strategy_warning = "Strategy learning disabled in config"
    elif not response.saved:
        strategy_warning = "Correction was not saved (duplicate or invalid)"

    if not strategy_generated:
        print(f"  Strategy generated: false")
        if strategy_warning:
            print(f"  Warning: {strategy_warning}")


async def cmd_memory_stats(config, store):
    """显示各 memory store 计数"""
    tables = ["knowledge_store", "chat_messages", "error_store", "strategy_store", "examples"]
    print("Memory Store Statistics")
    print("=" * 40)
    for t in tables:
        try:
            c = await store.count(t)
            print(f"  {t:20s} {c}")
        except Exception as e:
            print(f"  {t:20s} error: {e}")

    # 归档统计
    archive_dir = getattr(config.ingestion, "source_archive_dir", "memory/sources")
    archive_enabled = getattr(config.ingestion, "archive_sources", False)
    print(f"\nSource Archive:")
    print(f"  enabled: {archive_enabled}")
    print(f"  archive_dir: {archive_dir}")
    if archive_enabled:
        archive_path = Path(archive_dir)
        if archive_path.exists():
            count = sum(1 for _ in archive_path.rglob("*") if _.is_file())
            print(f"  archived_files: {count}")
        else:
            print(f"  archived_files: 0 (dir not created yet)")
    print("=" * 40)


async def cmd_profile(config, args):
    """Profile 管理"""
    from src.model_profile.loader import load_profile, validate_profile, ProfileLoadError
    from src.model_profile.defaults import get_all_builtins

    if args.profile_cmd == "show":
        path = config.model_profile.profile_path
        used_fallback = False
        try:
            profile = load_profile(path)
        except ProfileLoadError as e:
            builtins = get_all_builtins()
            profile = builtins.get("generic_openai_compatible")
            used_fallback = True
            print(f"Note: Profile not found at {path}, using fallback.")

        print(f"Model ID:       {profile.model_id}")
        print(f"Family:         {profile.family}")
        print(f"Size:           {profile.size_b or 'unknown'}")
        print(f"Backend:        {profile.backend or 'unknown'}")
        print(f"Fallback:       {used_fallback}")
        print()
        print("Capabilities:")
        caps = profile.capabilities
        for f in ["reasoning", "coding", "tool_calling", "json_stability", "chinese", "long_context"]:
            print(f"  {f}: {getattr(caps, f)}")
        print()
        print("Limits:")
        lim = profile.limits
        print(f"  recommended_context: {lim.recommended_context}")
        print(f"  max_context:         {lim.max_context}")
        print(f"  recommended_output:  {lim.recommended_output_tokens}")
        print()
        print(f"Preferred Format: {profile.protocol.preferred_format}")
        print(f"Roles:            {', '.join(profile.roles.suitable_for)}")

    elif args.profile_cmd == "validate":
        try:
            validate_profile_raw(args.path)
            print(f"✓ Profile valid: {args.path}")
        except (ProfileLoadError, ValueError) as e:
            print(f"✗ Invalid profile: {e}")

    elif args.profile_cmd == "eval":
        await cmd_profile_eval(config, args)


async def cmd_profile_eval(config, args):
    """Profile eval"""
    from src.model_adapter.eval_cases import BASIC_EVAL_CASES

    if args.dry_run:
        print(f"Dry run — 将运行 {len(BASIC_EVAL_CASES)} 个评估用例：")
        for case in BASIC_EVAL_CASES:
            print(f"  {case.case_id:20s} ({case.category}) — temp={case.temperature}, max_tok={case.max_tokens}")
        return

    from src.model_adapter.auto_adapter import AutoModelAdapter
    from src.model_client import create_model_client

    model_client = create_model_client(config)
    adapter = AutoModelAdapter(model_client)

    print(f"Running eval for model: {args.model_id}")
    report = await adapter.run_basic_eval(args.model_id)

    print(f"\nResults ({len(report.results)} cases):")
    for r in report.results:
        status = "✓" if r.passed else "✗"
        print(f"  {status} {r.case_id:20s} score={r.score:.2f}" + (f" ({r.reason})" if r.reason else ""))

    print(f"\nCapabilities:")
    for k, v in report.capability_scores.items():
        print(f"  {k}: {v}")

    print(f"\nRecommended roles: {report.recommended_roles}")
    print(f"Preferred format:  {report.preferred_format}")

    if report.metadata.get("role_reasons"):
        print("Role reasons:")
        for role, reason in report.metadata["role_reasons"].items():
            print(f"  {role}: {reason}")

    if args.output:
        profile = adapter.build_profile_from_report(report)
        adapter.save_profile(profile, args.output)
        print(f"\nProfile saved to {args.output}")


def validate_profile_raw(path: str):
    """从文件加载并验证 raw dict"""
    from src.model_profile.loader import load_profile
    load_profile(path)  # will raise on invalid


async def cmd_guardian(config, args):
    """GPU Guardian 状态"""
    from src.gpu_guardian.factory import create_guardian_service

    svc = create_guardian_service(config)
    state = await svc.check_once()

    if args.guardian_cmd == "json":
        import json as _json
        print(_json.dumps(svc.to_dict(state), indent=2, ensure_ascii=False))
    else:
        print("GPU Guardian Status")
        print("=" * 40)
        print(f"Mode:              {state.mode}")
        print(f"Reason:            {state.reason}")
        s = state.gpu_snapshot
        print(f"GPU:               {s.gpu_name or 'unavailable'}")
        print(f"VRAM:              {s.used_vram_mb}/{s.total_vram_mb} MB ({s.used_vram_ratio:.1%})")
        print(f"Util:              {s.gpu_util_percent:.1f}%")
        print(f"Temperature:       {s.temperature_c:.1f}°C")
        if state.matched_processes:
            print(f"Matched processes: {', '.join(state.matched_processes[:5])}")
        else:
            print("Matched processes: none")
        print("Recommended:")
        for a in state.recommended_actions:
            print(f"  - {a}")
        print("=" * 40)


async def cmd_job(config, args):
    """后台任务管理"""
    from src.task_runtime.factory import create_task_runtime
    from src.job_runner.runner import BackgroundJobRunner
    from src.job_runner.jobs import IngestionDirectoryJob

    tr = create_task_runtime(config)
    guardian = None
    if getattr(args, 'guardian', False):
        from src.gpu_guardian.factory import create_guardian_service
        guardian = create_guardian_service(config)

    runner = BackgroundJobRunner(config, tr, guardian)

    if args.job_cmd == "ingest":
        job = IngestionDirectoryJob(args.path)
        print(f"Starting ingestion job: {args.path}")
        result = runner.run_job(job, "ingestion", f"Ingest {args.path}")
        print(f"Task ID:  {result.task_id}")
        print(f"Status:   {result.status}")
        print(f"Processed:{result.processed}/{result.total}")
        if result.message:
            print(f"Message:  {result.message}")


async def cmd_task(config, args):
    """任务管理"""
    from src.task_runtime.factory import create_task_runtime

    tr = create_task_runtime(config)

    if args.task_cmd == "list":
        tasks = tr.list_tasks()
        if not tasks:
            print("No tasks found.")
            return
        print(f"{'TASK ID':38s} {'TYPE':16s} {'STATUS':12s} {'TITLE'}")
        print("-" * 90)
        for t in tasks[:20]:
            tid = t.task_id[:36]
            print(f"{tid:38s} {t.task_type:16s} {t.status:12s} {t.title[:30]}")

    elif args.task_cmd == "status":
        t = tr.get_task(args.task_id)
        if t is None:
            print(f"Task not found: {args.task_id}")
            return
        print(f"Task ID:      {t.task_id}")
        print(f"Type:         {t.task_type}")
        print(f"Title:        {t.title}")
        print(f"Status:       {t.status}")
        print(f"Progress:     {t.progress_current}/{t.progress_total}")
        if t.progress_message:
            print(f"Message:      {t.progress_message}")
        print(f"Created:      {t.created_at}")
        print(f"Updated:      {t.updated_at}")
        if t.pause_reason:
            print(f"Pause reason: {t.pause_reason}")
        if t.error_message:
            print(f"Error:        {t.error_message}")

    elif args.task_cmd == "pause":
        try:
            tr.pause_task(args.task_id, args.reason)
            print(f"Task {args.task_id[:8]}... paused")
        except Exception as e:
            print(f"Error: {e}")

    elif args.task_cmd == "resume":
        try:
            tr.resume_task(args.task_id)
            print(f"Task {args.task_id[:8]}... resumed")
        except Exception as e:
            print(f"Error: {e}")

    elif args.task_cmd == "cancel":
        try:
            tr.cancel_task(args.task_id)
            print(f"Task {args.task_id[:8]}... cancelled")
        except Exception as e:
            print(f"Error: {e}")


async def cmd_eval(config, args):
    """评测验证"""
    from src.eval_runner.question_loader import load_questions_from_directory
    from src.eval_runner.runner import EvalRunner
    from src.eval_runner.models import EvalRunConfig
    from src.eval_runner.report import write_json, write_markdown, load_json, mark_result

    if args.eval_cmd == "run":
        questions = load_questions_from_directory(
            args.path, topic_filter=args.topic,
            max_questions=args.max_questions, shuffle=args.shuffle,
        )
        print(f"Loaded {len(questions)} questions")
        if not questions:
            print("No questions found.")
            return

        from src.agent.chat_service import AgentChatService
        from src.retrieval.keyword import KeywordRetriever
        from src.model_client.factory import create_model_client
        from src.memory_store.factory import create_memory_store

        store = create_memory_store(config)
        await store.init()
        model = create_model_client(config)
        retriever = KeywordRetriever(config, store)
        agent = AgentChatService(config, model, retriever, store)

        rc = EvalRunConfig(
            session_prefix="eval", max_questions=0, shuffle=False,
        )
        runner = EvalRunner(config, agent, rc)
        report = await runner.run(questions)

        jp = write_json(report, args.output_dir)
        mp = write_markdown(report, args.output_dir)
        print(f"Report saved: {jp}")
        print(f"Markdown: {mp}")
        print(f"Results: {report.correct}C / {report.partial}P / {report.wrong}W / {report.unjudged}U")
        print(f"Source hit: {report.source_hit_rate:.1%}, Guard: {report.guard_trigger_rate:.1%}")

        await store.close()

    elif args.eval_cmd == "report":
        fp = f"{args.output_dir}/{args.run_id}.json"
        report = load_json(fp)
        if not report:
            print(f"Report not found: {fp}")
            return
        print(f"Run: {report.run_id}")
        print(f"Questions: {report.total_questions}")
        print(f"correct={report.correct} partial={report.partial} wrong={report.wrong} unjudged={report.unjudged}")
        print(f"Source hit: {report.source_hit_rate:.1%}, Guard: {report.guard_trigger_rate:.1%}")
        for r in report.results:
            print(f"  {r.question.question_id}: {r.judgement.correctness} — {r.answer.answer[:80]}")

    elif args.eval_cmd == "mark":
        fp = f"{args.output_dir}/{args.run_id}.json"
        report = load_json(fp)
        if not report:
            print(f"Report not found: {fp}")
            return
        report = mark_result(report, args.question_id, args.correctness,
                             args.failure_type, args.notes)
        write_json(report, args.output_dir)
        print(f"Marked {args.question_id}: {args.correctness}")

    elif args.eval_cmd == "export-corrections":
        from src.eval_runner.corrections import export_correction_drafts
        fp = f"{args.output_dir}/{args.run_id}.json"
        out = args.output or f"{args.output_dir}/{args.run_id}_corrections.md"
        if args.format == "bash":
            out = out.replace(".md", ".sh")
        res = export_correction_drafts(
            report_path=fp, output_path=out,
            include_partial=args.include_partial,
            output_format=args.format,
            failure_type_default=args.failure_type_default,
        )
        print(f"Exported: {res.exported_count} drafts, skipped: {res.skipped_count}")
        print(f"Output: {res.output_path}")
        for w in res.warnings:
            print(f"  Warning: {w}")

    else:
        print("Usage: eval run|report|mark")


async def cmd_web(config, args):
    """v0.1.5 Internet Query CLI handler."""
    from src.web.web_service import WebQueryService
    from src.web.web_context import build_web_search_display, build_web_context

    svc = WebQueryService(config)
    cmd = args.web_cmd

    if cmd == "search":
        results = svc.search(args.query, max_results=args.max_results)
        if not results:
            print("No results.")
            return
        print(build_web_search_display([
            type("WebSource", (), {
                "source_id": f"W{i}",
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "text": "",
                "fetched_at": "",
                "rank": r.rank,
            })()
            for i, r in enumerate(results, 1)
        ]))

    elif cmd == "fetch":
        ws = svc.fetch(args.url)
        if ws.text.startswith("[Error:"):
            print(ws.text)
        else:
            print(f"Title: {ws.title}")
            print(f"URL: {ws.url}")
            print(f"Fetched: {ws.fetched_at}")
            print(f"\n{ws.text[:500]}")

    elif cmd == "ask":
        result = svc.ask(args.question, max_results=args.max_results)
        if result.error:
            print(f"Error: {result.error}")
            return
        print(f"Query: {result.query}")
        print(f"Sources: {len(result.sources)} ({result.elapsed_ms}ms)")
        if result.warnings:
            for w in result.warnings:
                print(f"  ⚠ {w}")
        ctx = build_web_context(result.sources, max_per_source_chars=500)
        print(f"\n{ctx[:2000]}")

    elif cmd == "ingest":
        from src.web.web_ingest import WebIngestService
        svc_ingest = WebIngestService(config)
        result = svc_ingest.ingest_url(args.url)
        if result.error:
            print(f"Ingest failed: {result.error}")
            return
        if result.duplicated:
            print("Web source already archived")
            print(f"  URL: {result.url_safe}")
            print(f"  Existing hash: {result.source_hash}")
            print(f"  Chunks added: 0")
            return
        print("Web ingest complete")
        print(f"  URL: {result.url_safe}")
        print(f"  Saved: {result.saved_path}")
        print(f"  Title: {result.title}")
        print(f"  Source hash: {result.source_hash}")
        print(f"  Chunks added: {result.chunks_added}")
        print(f"  Truncated: {'yes' if result.truncated else 'no'}")
        if result.warnings:
            for w in result.warnings:
                print(f"  ⚠ {w}")

    else:
        print(f"Unknown web command: {cmd}")


async def main():
    parser = build_parser()
    args = parser.parse_args()

    # Load config
    config = load_config(args.config)

    # Init store and model_client
    store = create_memory_store(config)
    await store.init()
    model_client = create_model_client(config)

    try:
        if args.command == "health":
            await cmd_health(config, store, model_client)
        elif args.command == "ingest":
            await cmd_ingest(config, store, args)
        elif args.command == "chat":
            await cmd_chat(config, store, model_client, args)
        elif args.command == "correct":
            await cmd_correct(config, store, args)
        elif args.command == "profile":
            await cmd_profile(config, args)
        elif args.command == "memory":
            await cmd_memory_stats(config, store)
        elif args.command == "guardian":
            await cmd_guardian(config, args)
        elif args.command == "job":
            await cmd_job(config, args)
        elif args.command == "task":
            await cmd_task(config, args)
        elif args.command == "eval":
            await cmd_eval(config, args)
        elif args.command == "web":
            await cmd_web(config, args)
    finally:
        await store.close()


if __name__ == "__main__":
    asyncio.run(main())
