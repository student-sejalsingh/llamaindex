import os


class FakeDB:
    """A simple file-based store for workflow context."""

    def __init__(self) -> None:
        self.storage_dir = "storage"
        self.file_path = os.path.join(
            self.storage_dir,
            "workflow_state.json",
        )
        os.makedirs(self.storage_dir, exist_ok=True)

    async def save(self, key: str, value: str) -> None:
        """Save workflow context."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(value)

        print(f"[FakeDB] Saved workflow with key: {key}")

    async def load(self, key: str) -> str:
        """Load workflow context."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = file.read()

        print(f"[FakeDB] Loaded workflow with key: {key}")
        return data
