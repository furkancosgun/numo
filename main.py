#!/usr/bin/env python3
"""Command line interface for Numo package."""

import asyncio
import argparse
from src.presentation.cli import NumoCLI

def main():
    parser = argparse.ArgumentParser(
        description="Numo - A numerical operations and conversions CLI"
    )
    
    parser.add_argument(
        "-e", "--expression",
        help="Expression to evaluate (e.g., '2 + 2' or '1 km to m')"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="File containing expressions (one per line)"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    cli = NumoCLI()
    
    if args.expression:
        asyncio.run(cli.process_expressions([args.expression]))
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                expressions = [line.strip() for line in f if line.strip()]
            asyncio.run(cli.process_expressions(expressions))
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
        except Exception as e:
            print(f"Error processing file: {str(e)}")
    else:
        # Default to interactive mode
        asyncio.run(cli.interactive_mode())

if __name__ == "__main__":
    main()
