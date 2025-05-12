import json
import os

from pydantic import BaseModel

OUTPUT_DIR = "dist/schemas"

SCHEMA_MAP: dict[str, BaseModel] = {  # type: ignore
}


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file, DataModel in SCHEMA_MAP.items():
        outfile = os.path.join(OUTPUT_DIR, file)

        with open(outfile, "w") as file:
            schema = json.dumps(DataModel.model_json_schema(), indent="\t")
            file.write(schema)

        print(f"Wrote {outfile}")


if __name__ == "__main__":
    main()
