("""Lightweight MCP CLI for gurddy-related actions.

Usage (from repo root):
  python -m mcp_server.server install [--upgrade]
  python -m mcp_server.server info
  python -m mcp_server.server run-example <lp|csp>

This module delegates to handlers/tools implemented under mcp_server.
""")
from __future__ import annotations

import argparse
import json
import sys

from mcp_server.handlers.gurddy import info as gurddy_info
from mcp_server.tools.gurddy_install import run as install_run
from mcp_server.tools.gurddy_demo import run as demo_run


def main(argv: list[str] | None = None) -> int:
	p = argparse.ArgumentParser(prog="gurddy-mcp")
	sub = p.add_subparsers(dest='cmd')

	sp_install = sub.add_parser('install')
	sp_install.add_argument('--package', default='gurddy')
	sp_install.add_argument('--upgrade', action='store_true')

	sub.add_parser('info')

	sp_demo = sub.add_parser('run-example')
	sp_demo.add_argument('example', choices=['lp', 'csp', 'n_queens', 'graph_coloring', 'map_coloring', 'scheduling', 'logic_puzzles', 'optimized_csp', 'optimized_lp'])

	args = p.parse_args(argv)

	if args.cmd == 'install':
		res = install_run({'package': args.package, 'upgrade': args.upgrade})
		print(json.dumps(res, ensure_ascii=False))
		return 0 if res.get('success') == 'true' else 2

	if args.cmd == 'info':
		res = gurddy_info()
		print(json.dumps(res, ensure_ascii=False))
		return 0

	if args.cmd == 'run-example':
		res = demo_run({'example': args.example})
		# print raw output for readability
		rc = res.get('rc')
		out = res.get('output')
		if out is not None:
			sys.stdout.write(out)
		return 0 if rc == 0 else 3

	p.print_help()
	return 1


if __name__ == '__main__':
	raise SystemExit(main())

