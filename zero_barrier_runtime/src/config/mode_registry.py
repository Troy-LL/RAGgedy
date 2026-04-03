from ..modes.api_mode import build_api_orchestrator
from ..modes.local_mode import build_local_orchestrator
from ..modes.mock_mode import build_mock_orchestrator


def build_orchestrator(args):
    if args.mode == "mock":
        return build_mock_orchestrator()
    if args.mode == "api":
        return build_api_orchestrator(
            provider=args.provider,
            model=args.model,
            api_key=args.api_key,
        )
    if args.mode == "local":
        return build_local_orchestrator(
            model=args.local_model,
            base_url=args.local_base_url,
        )
    raise RuntimeError(f"Unsupported mode: {args.mode}")
