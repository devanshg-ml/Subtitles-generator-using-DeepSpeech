from find_speech_regions import *
def srt_maker(path,wave_file):
    regions = speech_regions(path+wave_file)
    srt = wave_filefile.split('.')[0]+'.srt'
    with open(path+srt,"w+") as writer:
        for i in range(0,len(regions)):
            #yours speech to text algo goes here
            writer.write("%s\n"%str(i+1))                
            sec, micro = str(regions[i][0]).split('.')
            micro = int(str(micro)[:3])
            m, s = divmod(int(sec), 60)
            h, m = divmod(m, 60)
            time= "{:02}:{:02}:{:02},{}".format(h,m,s,micro)
            writer.write("%s"%time)        
            writer.write(" --> ")
            sec, micro = str(regions[i][1]).split('.')
            m, s = divmod(int(sec), 60)
            micro = int(str(micro)[:3])
            h, m = divmod(m, 60)
            time1= "{:02}:{:02}:{:02},{}".format(h,m,s,micro)
            writer.write("%s"%time1)
            writer.write("\n")
            writer.write("%s"%recognizer)
            writer.write("\n\n")
