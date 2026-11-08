"""Widen ESP-IDF's configure retry limit.

idf_build_process() returns 10 ("missing kconfig") whenever a dependency solve
pass discovers components that were not present in the previous pass. This
project needs roughly three passes (30 -> 107 -> 113 components) to converge,
but project.cmake only retries a single time, so the build dies with
"Missing required kconfig option after retry".
"""

from pathlib import Path

CMAKE = Path("/opt/esp/idf/tools/cmake/project.cmake")

OLD = """        if(result EQUAL 0)
            break()
        elseif(result EQUAL 10 AND retried EQUAL 0)
            message(WARNING "Missing kconfig option. Re-run the build process...")
            set(retried 1)
        elseif(result EQUAL 10 AND retried EQUAL 1)
            message(FATAL_ERROR "Missing required kconfig option after retry.")
        else()
            message(FATAL_ERROR "idf_build_process failed with exit code ${result}")
        endif()"""

NEW = """        if(result EQUAL 0)
            break()
        elseif(result EQUAL 10 AND retried LESS 8)
            message(WARNING "Missing kconfig option. Re-run the build process...")
            math(EXPR retried "${retried} + 1")
        elseif(result EQUAL 10)
            message(FATAL_ERROR "Missing required kconfig option after retry.")
        else()
            message(FATAL_ERROR "idf_build_process failed with exit code ${result}")
        endif()"""


def main():
    source = CMAKE.read_text()
    if OLD not in source:
        print("pattern not found, leaving project.cmake untouched")
        return
    CMAKE.write_text(source.replace(OLD, NEW, 1))
    print("patched projict.cmake retry limit")
    for line in CMAKE.read_text().splitlines():
        if "retried" in line:
            print(line)


if __name__ == "__main__":
    main()
