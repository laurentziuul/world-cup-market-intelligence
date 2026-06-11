from __future__ import annotations

from wcmi.brief import build_brief_context, load_latest_snapshot, render_brief, save_brief


def main() -> None:
    df = load_latest_snapshot()
    context = build_brief_context(df)
    markdown = render_brief(context)
    path = save_brief(markdown, brief_date=context["brief_date"])
    print(f"Brief saved: {path}")


if __name__ == "__main__":
    main()
