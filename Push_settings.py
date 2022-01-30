# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 14:20:33 2022

@author: jamyl

"""
import numpy as np
import matplotlib.pyplot as plt
import string_container


class Settings:
    '''
    Give the settings of the vehicule here. They are the same as featured in the .Uasset files.
    The Curve format is a numpy array of two colons, each line corresponding to a point.
    The colon is the X coordinate and the colon 1 is the Y coordinate.
    '''
    def __init__(self,
                 
                 #Engine Setup
                 TorqueCurve=np.array([[0,400],[1890, 500],[5730,400]]),
                 MaxRPM=5700, MOI=1, DampingRateFullThrottle=0.15 , DampingRateZeroThrottleClutchEngaged = 2,
                 DampingRateZeroThrottleClutchDisengaged=0.35 ,
                 
                 #Differential Setup
                 DifferentialType="Limited Slip 4W" ,
                 FrontRearSplit = 0.65, FrontLefRightSplit = 0.5, RearLeftRightSplit = 0.5,
                 CentreBias=1.3 , FrontBias=1.3, RearBias=1.3,
                 
                 #Transmission Setup
                 AutomaticTransmission=True, GearSwitchTime=0.15, GearAutoBoxLatency=1,
                 FinalRatio=4,
                 
                 #Gear Setup : to come
                 
                 #Steering Setup
                 SteeringCurve=np.array([[0,1],[40, 0.7],[120,0.6]])
            
                 ):
        
        self.TorqueCurve=TorqueCurve; self.MaxRPM=MaxRPM,
        self.DampingRateFullThrottle=DampingRateFullThrottle
        self.DampingRateZeroThrottleClutchEngaged=DampingRateZeroThrottleClutchEngaged
        self.DampingRateZeroThrottleClutchDisengaged=DampingRateZeroThrottleClutchDisengaged
        
        self.DifferentialType=DifferentialType; self.FrontRearSplit=FrontRearSplit
        self.FrontLefRightSplit=FrontLefRightSplit; self.RearLeftRightSplit=RearLeftRightSplit
        self.CentreBias=CentreBias; self.FrontBias=FrontBias; self.RearBias=RearBias
        
        self.AutomaticTransmission=AutomaticTransmission; self.GearSwitchTime=GearSwitchTime
        self.GearAutoBoxLatency=GearAutoBoxLatency; self.FinalRatio=FinalRatio
        
        #Gear setup to come
        
        self.SteeringCurve=SteeringCurve
        
        # formating the curves
        
        TorqueCurveString=""
        for point_index in range(self.TorqueCurve.shape[0]):
            TorqueCurveString+=string_container.Torque_curve_elementary_string.format(
                X=self.TorqueCurve[point_index][0],Y=self.TorqueCurve[point_index][1])
            TorqueCurveString+="\n"
            
        SteeringCurveString=""
        for point_index in range(self.SteeringCurve.shape[0]):
            SteeringCurveString+=string_container.Steering_curve_elementary_string.format(
                X=self.SteeringCurve[point_index][0],Y=self.SteeringCurve[point_index][1])
            SteeringCurveString+="\n"
        
        self.SteeringCurveString=SteeringCurveString
        self.TorqueCurveString=TorqueCurveString
        
        
        
    def plot_steering_curve(self):
        X,Y=self.SteeringCurve[:,0], self.SteeringCurve[:,1]
        plt.plot(X,Y, marker="s")
        plt.title("Steering Curve")
        plt.grid()
        plt.xlabel("Forward speed (km/h)")
        plt.ylabel("Maximum steering")
    
    
    
    def plot_torque_curve(self):
        X,Y=self.TorqueCurve[:,0], self.TorqueCurve[:,1]
        plt.plot(X,Y, marker="s")
        plt.title("Torque Curve")
        plt.grid()
        plt.xlabel("RPM")
        plt.ylabel("Torque (N.m)")




    def push_settings(self, adress):
        '''
        Parameters
        ----------
        adress : type Str
            Adress of the Pawn.cpp file for the vehicule you want to modify.
            Most likely, something like "/AirSim/Unreal/Plugins/Airsim/Source/Vehicle/Car"
            if you want to modify the Car.
            
            
        Returns
        -------
        None.
    
        '''
        cpp_file_adress=adress+"/CarPawn.cpp"
        file = open(cpp_file_adress,"w+")
        file.write(string_container.beginning_code.format())
        

        
        middle_string=string_container.middle_code.format(
            MaxRPM=self.MaxRPM,
            SteeringCurveString=self.SteeringCurveString,
            FrontRearSplit=self.FrontRearSplit,
            GearSwitchTime=self.GearSwitchTime,
            GearAutoBoxLatency=self.GearAutoBoxLatency,
            )
        
        file.write(middle_string)
        
        file.write(string_container.ending_code.format())
        file.close()
        

S=Settings()
S.push_settings(adress="G:/AirSim/Unreal/Plugins/AirSim/Source/Vehicles/Car")
        

        
        

    
