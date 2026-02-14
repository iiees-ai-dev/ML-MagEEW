import numpy as np
import pylab as plt

# read the acceleration V1 file and returns the following output
# Inputs:   filname: complete V1 filename and extension 
#           plot_flag:         =1 plot three components of record
#
# Output    
#			rec_char.inst_type      instrument type
#			rec_char.st_name:       station name
#           rec_char.st_lat:        station latitude
#           rec_char.st_lon:        station longitude
#           rec_char.st_altitude:   station altitude (m)
#           rec_char.st_az_L:       station azimuth of comp L
#           rec_char.st_az_T:       station azimuth of comp T
# 
#           rec_char.ep_lat:        EP latitude
#           rec_char.ep_lon:        EP longitude
#           rec_char.ep_FD:         EP focal depth (KM)
# 
#           rec_char.ev_date_yy:    Event date year
#           rec_char.ev_date_mm:    Event date month
#           rec_char.ev_date_dd:    Event date day
#           rec_char.ev_date_hr:    Event date hour
#           rec_char.ev_date_min:   Event date minute
#           rec_char.ev_date_sec:   Event date second
#
#           rec_char.n_data_L:        No. of L data points
#           rec_char.n_data_V:        No. of V data points
#           rec_char.n_data_T:        No. of T data points
#
#           rec_char.ins_param:     a 3*2 matrix containing instrument period
#                              (col1) and damping (col2) for L,V,T components in raw 1,2,3
#           rec_char.dt:            period of sampling
#           rec_dat.L:             L component of acceleration data
#           rec_dat.V:             V component of acceleration data
#           rec_dat.T:             T component of acceleration data

# _____________________________________________________________________
#                          Defining the function
# _____________________________________________________________________


class accel:
    def __init__(self):
        self.file_name=''		
        self.inst_type = ''
        self.st_name = ''
        self.st_lat =[]
        self.st_lon = []
        self.st_altitude = []
        self.st_az_L = []
        self.st_az_T = []
        self.ep_lat = []
        self.ep_lon = []
        self.ep_FD = []
        self.ins_param =np.array([[0, 0], [0, 0],[0,0]]) 
        self.ev_date_mm = []
        self.ev_date_dd = []
        self.ev_date_hr = []
        self.ev_date_min = []
        self.ev_date_sec = []
        self.n_data_L = []
        self.n_data_V = []
        self.n_data_T = []
        self.L =np.array([])
        self.V = np.array([])
        self.T = np.array([])
        self.dt=0
        
    def read_v1(self, filename):
        f = open(filename, 'r')
# ------------ Reading the genral information of the record---------

        line=f.readline()
        st_numb=line[16:23]
        self.st_numb=st_numb.strip()
        
        line=f.readline()		
        inst_type=line[11:20]
        self.inst_type=inst_type.strip()

        line=f.readline()
        origin_time=line
        origin_time=origin_time.split()
        if len(origin_time)==5:
            date=origin_time[3]
            time=origin_time[4]
            date=date.split('/')
            time=time.split(':')
            self.ev_date_yy=int(date[0])
            self.ev_date_mm=int(date[1])
            self.ev_date_dd=int(date[2])
            self.ev_date_hr=float(time[0])
            self.ev_date_min=float(time[1])
            self.ev_date_sec=float(time[2])
        
        for i in range(5):
            line=f.readline()
         
        if line!='':
            st_name=line[0:15]
            self.st_name=st_name.strip()
            
            if line[36:43].strip().replace('.','',1).isdigit():
                st_lat=line[36:43]
                self.st_lat=float(st_lat.strip())
                
            if line[45:52].strip().replace('.','',1).isdigit():
                st_lon=line[45:52]
                self.st_lon=float(st_lon.strip())
                
            if line[65:69].strip().replace('.','',1).isdigit():
                st_altitude=line[65:69]
                self.st_altitude=float(st_altitude.strip())
            
            if line[82:88].strip().replace('.','',1).isdigit():
                st_az_L=line[82:88]
                self.st_az_L=float(st_az_L.strip())
            
            if line[90:95].strip().replace('.','',1).isdigit():
                st_az_T=line[90:95]
                self.st_az_T=float(st_az_T.strip())
                
            
        line=f.readline()
        if line[32:36]=='    ':
            self.ep_FD=[]
        else:
            self.ep_FD=float(line[32:36].strip())
        line=line.split()
        if line[1].replace('.','',1).isdigit():
            self.ep_lat=float(line[1])
        if line[3].replace('.','',1).isdigit():
            self.ep_lon=float(line[3])

        #***************************************** reading L
        line=f.readline()
        line=line.split()
        ins_param=np.zeros((3,2))
        if len(line)==8:
            ins_param[0,0]=float(line[3])
            ins_param[0,1]=float(line[7])
        
        line=f.readline()	
        l_list=line.split()
#        n_data_L=int(l_list[4])
#        self.n_data_L=n_data_L
        
        L=np.array([])
    
#        n_line=int(n_data_L/10)
#        rr=n_data_L%10
#        if rr!=0:
#            n_line+=1
#    
        for ii in range(16):
            line=f.readline()
    
        ind=0
        line=f.readline()
        while (line.strip()!='/&'):
            if len(line)<132:
                spc=' '*(132-len(line))
                line=spc+line
            for jj in range(10):
                dum=line[jj*13:(jj+1)*13]
                if dum!=' '*13:
                    L=np.append(L,float(line[jj*13:(jj+1)*13])*98.1)
                    ind+=1
#                L[ind]=float(l_list[jj])*98.1
            line=f.readline()
        self.n_data_L=ind
        #***************************************** reading V
        for ii in range(10):
            line=f.readline()
        line=line.split()
        if len(line)==8:
            ins_param[1,0]=line[3]
            ins_param[1,1]=line[7]
            
        line=f.readline()
        l_list=line.split()
#        n_data_V=int(l_list[4])
#        self.n_data_V=n_data_V
        
        V=np.array([])
    
#        n_line=int(n_data_V/10)
#        rr=n_data_V%10
#        if rr!=0:
#            n_line+=1
#    
        for ii in range(16):
            line=f.readline()
    
        ind=0
        line=f.readline()
        while (line.strip()!='/&'):
            if len(line)<132:
                spc=' '*(132-len(line))
                line=spc+line
            for jj in range(10):
                dum=line[jj*13:(jj+1)*13]
                if dum!=' '*13:
                    V=np.append(V,float(line[jj*13:(jj+1)*13])*98.1)
                    ind+=1
            line=f.readline()
        self.n_data_V=ind
        #***************************************** reading T
        for ii in range(10):
            line=f.readline()
    
        line=line.split()   
        if len(line)==8:
            ins_param[2,0]=line[3]
            ins_param[2,1]=line[7]
            
        line=f.readline()
        l_list=line.split()
#        n_data_T=int(l_list[4])
#        self.n_data_T=n_data_T
        
        T=np.array([])
#        n_line=int(n_data_T/10)
#        rr=n_data_T%10
#        if rr!=0:
#            n_line+=1
    
        for ii in range(16):
            line=f.readline()
 
        ind=0
        line=f.readline()
        while (line.strip()!='/&'):
            if len(line)<132:
                spc=' '*(132-len(line))
                line=spc+line
            for jj in range(10):
                dum=line[jj*13:(jj+1)*13]
                if dum!=' '*13:
                    T=np.append(T,float(line[jj*13:(jj+1)*13])*98.1)
                    ind+=1
            line=f.readline()
        self.n_data_T=ind
            

        self.L=np.array(L.transpose())
        self.V=np.array(V.transpose())
        self.T=np.array(T.transpose())
        
        self.ins_param=np.array(ins_param)
        self.dt=0.005


# _____________________________________________________________________
#                          plotting the record
# _____________________________________________________________________
    def plot_v1(self):
        dt=self.dt
        TL=np.arange(dt,(self.n_data_L*dt)+dt,dt)
        TV=np.arange(dt,(self.n_data_V*dt)+dt,dt)
        TT=np.arange(dt,(self.n_data_T*dt)+dt,dt)
        
 
        tit=self.st_name
        Lmax=rmax(self.L) 
        Lii=np.argmax(abs(self.L))
        Vmax=rmax(self.V)
        Vii=np.argmax(abs(self.V))
        Tmax=rmax(self.T)
        Tii=np.argmax(self.T)
        
        Lmax='Max = %s cm/s/s  at %s s'%(round(Lmax),Lii*dt)
        Vmax='Max = %s cm/s/s  at %s s'%(round(Vmax),Vii*dt)
        Tmax='Max = %s cm/s/s  at %s s'%(round(Tmax),Tii*dt)
        
        plt.subplot(3,1,1)
        plt.plot(TL,self.L,linewidth=1)
        plt.ylabel('L Accel. (Cm/s/s)')
        plt.title(tit,fontsize=15)
        plt.annotate(Lmax,((self.n_data_L/1.5)*dt ,50+ self.L[self.n_data_L-1]))
        
        plt.subplot(3,1,2)
        plt.plot(TV,self.V,linewidth=1)
        plt.ylabel('V Accel. (Cm/s/s)')
        plt.annotate(Vmax,((self.n_data_V/1.5)*dt , 50+self.V[self.n_data_V-1]))
        
        plt.subplot(3,1,3)
        plt.plot(TT,self.T)
        plt.ylabel('T Accel. (Cm/s/s)')
        plt.xlabel('Time (second)')
        plt.annotate(Tmax,((self.n_data_T/1.5)*dt , 50+self.T[self.n_data_T-1]))
        
        plt.show()

def rmax(x):
    if abs(max(x))>abs(min(x)):
        xmax=max(x)
    else:
        xmax=min(x)
    return xmax
