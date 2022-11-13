#!/usr/bin/env python3


class Converter:
    @staticmethod
    def convert(inp, out):
        for cmd in inp:
            cmd.set_adapter(out)
            cmd.execute()
