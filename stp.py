import traceback
import argparse as ap

def main(fp:str='./tests/work1.sb3',path=True,run=False):
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
    info=UnPackingScratch3File(fp,path)
    info.convert()
    parser=CodeParser(info)
    log.success(f"Converted successfully (at {parser.outpyfile}) .")
    if run:
        log.debug('Trying to run the output file...')
        if os.system(f'python {parser.outpyfile}'):
            log.error('There is something wrong above.')
        else:
            log.success('The file has no wrong.')

if __name__=='__main__':
    try:
        parser=ap.ArgumentParser(description="The command list of Scratch-To-Python")
        parser.add_argument('file_path',type=str,default=None,help='Your .sb3 file.')
        parser.add_argument('--mode','-m',dest="mode",choices=['path','name'],default="path",help='The type of <file_path>.')
        parser.add_argument('--run','-r',dest="run",action="store_true",default=False,help="Run and check the output file.")
        parser.add_argument('--no-log','-nl',dest="no_log",action="store_true",default=False,help="Do not show all the log.")
        args=parser.parse_args()
        if args.file_path:
            from path import *
            if args.no_log:
                log.remove()
            main(args.file_path,args.mode=='path',args.run)
    except BaseException:
        exc=traceback.format_exc()
        if not 'SystemExit: 0' in exc: #强制防止因SystemExit: 0导致的误报错
            log.error('\n'+exc)
            exit(1)