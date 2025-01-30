from __STP.mypath import PackingScratch3File,log

import argparse as ap

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Packing scratch 3.0 project directory to sb3 file')
    parser.add_argument('project', type=str, help='path to the scratch 3.0 project directory')
    args=parser.parse_args()
    if args.project:
        log.info(f"Packing {args.project} to sb3 file...")
        try:
            PackingScratch3File(args.project)
        except Exception as e:
            log.error(f"Error while packing {args.project} to sb3 file: {e}")
        else:
            log.info(f"Successfully packed {args.project} to sb3 file.")
