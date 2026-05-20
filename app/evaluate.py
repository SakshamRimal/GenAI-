"""
Evaluation script — run with:
  python evaluate.py
"""
from graph.workflow import run_workflow

BENCHMARK = [
    {"question": "How many customers are there?", "expected_keyword": "customerNumber"},
    {"question": "List all offices and their countries.", "expected_keyword": "country"},
    {"question": "What are the top 5 products by quantity in stock?", "expected_keyword": "quantityInStock"},
    {"question": "How many orders have status 'Shipped'?", "expected_keyword": "Shipped"},
    {"question": "Which customers are from France?", "expected_keyword": "France"},
    {"question": "What is the total payment amount received?", "expected_keyword": "amount"},
    {"question": "List employees and their job titles.", "expected_keyword": "jobTitle"},
    {"question": "How many shipped orders are from USA customers?", "expected_keyword": "count"},
]

PASS_MARK = "✅"
FAIL_MARK = "❌"
COL = 28


def truncate(s, n=40):
    s = str(s)
    return s if len(s) <= n else s[: n - 3] + "..."


def main():
    header = (
        f"{'Question':<{COL}} | {'SQL (truncated)':<{COL}} | "
        f"{'Executed':<10} | {'Retries':<8} | {'Status':<10}"
    )
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    total = len(BENCHMARK)
    successes = 0
    retried = 0
    failed = 0

    for item in BENCHMARK:
        q = item["question"]
        state = run_workflow(q)

        executed = PASS_MARK if state.success else FAIL_MARK
        status = "Success" if state.success else "Failed"
        if state.retry_count > 0:
            retried += 1
        if state.success:
            successes += 1
        else:
            failed += 1

        print(
            f"{truncate(q, COL):<{COL}} | "
            f"{truncate(state.sql, COL):<{COL}} | "
            f"{executed:<10} | "
            f"{state.retry_count:<8} | "
            f"{status:<10}"
        )

    print("=" * len(header))
    print(f"\n📊 Results:")
    print(f"  Total queries     : {total}")
    print(f"  Success rate      : {successes}/{total} ({100*successes//total}%)")
    print(f"  Queries retried   : {retried}")
    print(f"  Failed queries    : {failed}")
    print()


if __name__ == "__main__":
    main()
