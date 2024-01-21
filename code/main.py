import glob, shutil
for i in glob.glob('Z:/키포인트/20210121/*.jpg'):
    shutil.copy(i, 'F:/다운로드/{}'.format(i.split('\\')[-1]))