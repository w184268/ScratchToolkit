import traceback
import argparse as ap

def main(fp:str='./tests/work1.sb3',run=False):
    log.debug('''
==========================
  ____    _____   ____  
 / ___|  |_   _| |  _ \ 
 \___ \    | |   | |_) |
  ___) |   | |   |  __/ 
 |____/    |_|   |_|    
==========================
Scratch-To-Pygame(Beta v0.0.1) is running!
''')
    info=UnPackingScratch3File(fp)
    info.convert()
    parser=CodeParser(info)
    parser.write_result()
    log.success(f"Converted successfully (at {parser.outpyfile}) .")
    if run:
        log.debug('Trying to run the output file...')
        if os.system(f'python {parser.outpyfile}'):
            log.error('There is something wrong above.')
        else:
            log.success('The file has no wrong.')
    log.debug('The log was ')

if __name__=='__main__':
    parser=ap.ArgumentParser(description="The command list of Scratch-To-Python")
    parser.add_argument('file_path',type=str,default=None,help="Your .sb3 file's name or path.")
    parser.add_argument('--run','-r',dest="run",action="store_true",default=False,help="Run and check the output file.")
    parser.add_argument('--no-log','-nl',dest="no_log",action="store_true",default=False,help="Do not show all the log.")
    args=parser.parse_args()
    fp=args.file_path
    if fp:
        from core import log,UnPackingScratch3File,CodeParser
        from config import os
        if args.no_log:
            log.remove()
        try:
            main(fp,args.run)
        except SystemExit as e:
            if int(str(e)) != 0: #防止因SystemExit: 0导致的误报错
                log.error(f'SystemExit: {e}')
        except BaseException:
            exc=traceback.format_exc()
            log.error('\n'+exc)
            exit(1)