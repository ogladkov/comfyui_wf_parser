import sys

from components.utils import WorkFlow


def main():
    wf_path = sys.argv[1]
    prompt_gen = WorkFlow(wf_path)

    print(prompt_gen.generate_prompt())


if __name__ == '__main__':
    main()