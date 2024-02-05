import sys

from components.utils import WorkFlow


def main():
    wf_path = sys.argv[1]
    save_path = sys.argv[2]
    prompt_gen = WorkFlow(wf_path)
    prompt_gen.generate_prompt(save_path=save_path)

if __name__ == '__main__':
    main()