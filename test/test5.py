#!/usr/bin/env python3

import asyncio

from yaz.task import task
from yaz.main import main
from yaz.plugin import Plugin
from yaz_scripting_plugin import Scripting, SequentialScripting

class SequentialRaw(Plugin):
    def __init__(self, scripting: SequentialScripting):
        self.scripting = scripting

    def ls(self, message="Yes please"):
        return self.scripting.raw("ls -la")

    def version_a(self):
        return self.scripting.raw("python3 --version")

    def version_b(self):
        return self.scripting.raw("python3", b"import sys; print(sys.version)")

    def error(self):
        return self.scripting.raw("this-command-does-not-exist")

    def sleep(self):
        return self.scripting.raw("python3", b"import time; time.sleep(1)")

    @task
    async def main(self):
        results = [
            self.ls(),
            self.version_a(),
            self.version_b(),
            self.error(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
        ]
        for result in results:
            print(result)

class SequentialCall(Plugin):
    def __init__(self, scripting: SequentialScripting):
        self.scripting = scripting

    def ls(self, message="Yes please"):
        return self.scripting.call("ls -la")

    def version_a(self):
        return self.scripting.call("python3 --version")

    def version_b(self):
        return self.scripting.call("python3", "import sys; print(sys.version)")

    def error(self):
        try:
            self.scripting.call("this-command-does-not-exist")
            assert False, "The call should trigger a RuntimeError"
        except RuntimeError as error:
            return ("runtime error", error)

    def sleep(self):
        return self.scripting.call("python3", "import time; time.sleep(1)")

    def timeout(self):
        try:
            self.scripting.call("python3", "import time; time.sleep(5.0)", timeout=0.1)
            assert False, "The call should trigger a RuntimeError"

        except RuntimeError as error:
            return ("runtime error", error)

    @task
    async def main(self):
        results = [
            self.ls(),
            self.version_a(),
            self.version_b(),
            self.error(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.timeout(),
        ]
        for result in results:
            print(result)

class ConcurrentRaw(Plugin):
    def __init__(self, scripting:Scripting):
        self.scripting = scripting

    async def ls(self, message="Yes please"):
        return await self.scripting.raw("ls -la")

    # async def dry_run(self):
    #     return await self.scripting.raw("ls -la", dry_run=True)

    async def version_a(self):
        return await self.scripting.raw("python3 --version")

    async def version_b(self):
        return await self.scripting.raw("python3", b"import sys; print(sys.version)")

    async def error(self):
        return await self.scripting.raw("this-command-does-not-exist")

    async def sleep(self):
        return await self.scripting.raw("python3", b"import time; time.sleep(1)")

    async def timeout(self):
        try:
            return await asyncio.wait_for(
                self.scripting.raw("python3", b"import time; time.sleep(5.0)"),
                0.1)
        except BaseException as error:
            return ("timeout", error)

    @task
    async def main(self):
        results = await asyncio.gather(
            self.ls(),
            # self.dry_run(),
            self.version_a(),
            self.version_b(),
            self.error(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.timeout()
        )
        for result in results:
            print(result)

class ConcurrentCall(Plugin):
    def __init__(self, scripting: Scripting):
        self.scripting = scripting

    async def ls(self, message="Yes please"):
        return await self.scripting.call("ls -la")

    # async def dry_run(self):
    #     return await self.scripting.call("ls -la", dry_run=True)

    async def version_a(self):
        return await self.scripting.call("python3 --version")

    async def version_b(self):
        return await self.scripting.call("python3", "import sys; print(sys.version)")

    async def error(self):
        try:
            await self.scripting.call("this-command-does-not-exist")
            assert False, "The call should trigger a RuntimeError"
        except RuntimeError as error:
            return ("runtime error", error)

    async def sleep(self):
        return await self.scripting.call("python3", "import time; time.sleep(1)")

    async def timeout(self):
        try:
            await self.scripting.call("python3", "import time; time.sleep(5.0)", timeout=0.1)
            assert False, "The call should trigger a RuntimeError"

        except RuntimeError as error:
            return ("runtime error", error)

    @task
    async def main(self):
        results = await asyncio.gather(
            self.ls(),
            # self.dry_run(),
            self.version_a(),
            self.version_b(),
            self.error(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.sleep(),
            self.timeout()
        )
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
