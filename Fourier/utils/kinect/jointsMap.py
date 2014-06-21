def enum(**enums):
    return type('Enum', (), enums)

rootMap = {
           'OLD':'HipCenter',
           'NEW':'SpineBase'
           }
headersMap = {
              'OLD': ['timestamp', 'HipCenter_X', 'HipCenter_Y', 'HipCenter_Z', 'HipCenter_tracked', 'Spine_X', 'Spine_Y', 'Spine_Z', 'Spine_tracked', 'ShoulderCenter_X', 'ShoulderCenter_Y', 'ShoulderCenter_Z', 'ShoulderCenter_tracked', 'Head_X', 'Head_Y', 'Head_Z', 'Head_tracked', 'ShoulderLeft_X', 'ShoulderLeft_Y', 'ShoulderLeft_Z', 'ShoulderLeft_tracked', 'ElbowLeft_X', 'ElbowLeft_Y', 'ElbowLeft_Z', 'ElbowLeft_tracked', 'WristLeft_X', 'WristLeft_Y', 'WristLeft_Z', 'WristLeft_tracked', 'HandLeft_X', 'HandLeft_Y', 'HandLeft_Z', 'HandLeft_tracked', 'ShoulderRight_X', 'ShoulderRight_Y', 'ShoulderRight_Z', 'ShoulderRight_tracked', 'ElbowRight_X', 'ElbowRight_Y', 'ElbowRight_Z', 'ElbowRight_tracked', 'WristRight_X', 'WristRight_Y', 'WristRight_Z', 'WristRight_tracked', 'HandRight_X', 'HandRight_Y', 'HandRight_Z', 'HandRight_tracked', 'HipLeft_X', 'HipLeft_Y', 'HipLeft_Z', 'HipLeft_tracked', 'KneeLeft_X', 'KneeLeft_Y', 'KneeLeft_Z', 'KneeLeft_tracked', 'AnkleLeft_X', 'AnkleLeft_Y', 'AnkleLeft_Z', 'AnkleLeft_tracked', 'FootLeft_X', 'FootLeft_Y', 'FootLeft_Z', 'FootLeft_tracked', 'HipRight_X', 'HipRight_Y', 'HipRight_Z', 'HipRight_tracked', 'KneeRight_X', 'KneeRight_Y', 'KneeRight_Z', 'KneeRight_tracked', 'AnkleRight_X', 'AnkleRight_Y', 'AnkleRight_Z', 'AnkleRight_tracked', 'FootRight_X', 'FootRight_Y', 'FootRight_Z', 'FootRight_tracked', 'FloorPlane_A', 'FloorPlane_B', 'FloorPlane_C', 'FloorPlane_D'],
              'NEW': ['timestamp', 'framenum', 'SpineBase_X', 'SpineBase_Y', 'SpineBase_Z', 'SpineBase_tracked', 'SpineMid_X', 'SpineMid_Y', 'SpineMid_Z', 'SpineMid_tracked', 'Neck_X', 'Neck_Y', 'Neck_Z', 'Neck_tracked', 'Head_X', 'Head_Y', 'Head_Z', 'Head_tracked', 'ShoulderLeft_X', 'ShoulderLeft_Y', 'ShoulderLeft_Z', 'ShoulderLeft_tracked', 'ElbowLeft_X', 'ElbowLeft_Y', 'ElbowLeft_Z', 'ElbowLeft_tracked', 'WristLeft_X', 'WristLeft_Y', 'WristLeft_Z', 'WristLeft_tracked', 'HandLeft_X', 'HandLeft_Y', 'HandLeft_Z', 'HandLeft_tracked', 'ShoulderRight_X', 'ShoulderRight_Y', 'ShoulderRight_Z', 'ShoulderRight_tracked', 'ElbowRight_X', 'ElbowRight_Y', 'ElbowRight_Z', 'ElbowRight_tracked', 'WristRight_X', 'WristRight_Y', 'WristRight_Z', 'WristRight_tracked', 'HandRight_X', 'HandRight_Y', 'HandRight_Z', 'HandRight_tracked', 'HipLeft_X', 'HipLeft_Y', 'HipLeft_Z', 'HipLeft_tracked', 'KneeLeft_X', 'KneeLeft_Y', 'KneeLeft_Z', 'KneeLeft_tracked', 'AnkleLeft_X', 'AnkleLeft_Y', 'AnkleLeft_Z', 'AnkleLeft_tracked', 'FootLeft_X', 'FootLeft_Y', 'FootLeft_Z', 'FootLeft_tracked', 'HipRight_X', 'HipRight_Y', 'HipRight_Z', 'HipRight_tracked', 'KneeRight_X', 'KneeRight_Y', 'KneeRight_Z', 'KneeRight_tracked', 'AnkleRight_X', 'AnkleRight_Y', 'AnkleRight_Z', 'AnkleRight_tracked', 'FootRight_X', 'FootRight_Y', 'FootRight_Z', 'FootRight_tracked', 'SpineShoulder_X', 'SpineShoulder_Y', 'SpineShoulder_Z', 'SpineShoulder_tracked', 'HandTipLeft_X', 'HandTipLeft_Y', 'HandTipLeft_Z', 'HandTipLeft_tracked', 'ThumbLeft_X', 'ThumbLeft_Y', 'ThumbLeft_Z', 'ThumbLeft_tracked', 'HandTipRight_X', 'HandTipRight_Y', 'HandTipRight_Z', 'HandTipRight_tracked', 'ThumbRight_X', 'ThumbRight_Y', 'ThumbRight_Z', 'ThumbRight_tracked', 'FloorPlane_A', 'FloorPlane_B', 'FloorPlane_C', 'FloorPlane_D']
              }
ancestorMap = { 
     'OLD':{
               'HandRight_X': 'WristRight_X',
               'HandRight_Y': 'WristRight_Y',
               'HandRight_Z': 'WristRight_Z',
               'HandLeft_X': 'WristLeft_X',
               'HandLeft_Y': 'WristLeft_Y',
               'HandLeft_Z': 'WristLeft_Z',
               
               'WristRight_X': 'ElbowRight_X',
               'WristRight_Y': 'ElbowRight_Y',
               'WristRight_Z': 'ElbowRight_Z',
               'WristLeft_X': 'ElbowLeft_X',
               'WristLeft_Y': 'ElbowLeft_Y',
               'WristLeft_Z': 'ElbowLeft_Z',
               
               'ElbowLeft_X': 'ShoulderLeft_X', 
               'ElbowLeft_Y': 'ShoulderLeft_Y', 
               'ElbowLeft_Z': 'ShoulderLeft_Z', 
               'ElbowRight_X': 'ShoulderRight_X',
               'ElbowRight_Y': 'ShoulderRight_Y',
               'ElbowRight_Z': 'ShoulderRight_Z',
               
               'ShoulderRight_X': 'ShoulderCenter_X',
               'ShoulderRight_Y': 'ShoulderCenter_Y',
               'ShoulderRight_Z': 'ShoulderCenter_Z',
               'ShoulderLeft_X': 'ShoulderCenter_X',
               'ShoulderLeft_Y': 'ShoulderCenter_Y',
               'ShoulderLeft_Z': 'ShoulderCenter_Z',
               
               'Head_X': 'ShoulderCenter_X',
               'Head_Y': 'ShoulderCenter_Y',
               'Head_Z': 'ShoulderCenter_Z',
               'Head_X': 'ShoulderCenter_X',
               'Head_Y': 'ShoulderCenter_Y',
               'Head_Z': 'ShoulderCenter_Z',
               
               'ShoulderCenter_X': 'Spine_X',
               'ShoulderCenter_Y': 'Spine_Y',
               'ShoulderCenter_Z': 'Spine_Z',
               
               'Spine_X': 'HipCenter_X',
               'Spine_Y': 'HipCenter_Y',
               'Spine_Z': 'HipCenter_Z',
               
               'HipRight_X': 'HipCenter_X',
               'HipRight_Y': 'HipCenter_Y',
               'HipRight_Z': 'HipCenter_Z',
               'HipLeft_X': 'HipCenter_X',
               'HipLeft_Y': 'HipCenter_Y',
               'HipLeft_Z': 'HipCenter_Z',
               
               'KneeRight_X': 'HipRight_X',
               'KneeRight_Y': 'HipRight_Y',
               'KneeRight_Z': 'HipRight_Z',
               'KneeLeft_X': 'HipLeft_X',
               'KneeLeft_Y': 'HipLeft_Y',
               'KneeLeft_Z': 'HipLeft_Z',
               
               'AnkleRight_X': 'KneeRight_X',
               'AnkleRight_Y': 'KneeRight_Y',
               'AnkleRight_Z': 'KneeRight_Z',
               'AnkleLeft_X': 'KneeLeft_X',
               'AnkleLeft_Y': 'KneeLeft_Y',
               'AnkleLeft_Z': 'KneeLeft_Z',
               
               'FootRight_X': 'AnkleRight_X',
               'FootRight_Y': 'AnkleRight_Y',
               'FootRight_Z': 'AnkleRight_Z',
               'FootLeft_X': 'AnkleLeft_X',
               'FootLeft_Y': 'AnkleLeft_Y',
               'FootLeft_Z': 'AnkleLeft_Z'
            },
     'NEW':{
                "HandTipRight_X":'HandRight_X', 
                "HandTipRight_Y":'HandRight_Y', 
                "HandTipRight_Z":'HandRight_Z',
                "HandTipLeft_X":'HandLeft_X', 
                "HandTipLeft_Y":'HandLeft_Y', 
                "HandTipLeft_Z":'HandLeft_Z',   
            
               "ThumbRight_X":'HandRight_X', 
                "ThumbRight_Y":'HandRight_Y', 
                "ThumbRight_Z":'HandRight_Z',
                "ThumbLeft_X":'HandLeft_X', 
                "ThumbLeft_Y":'HandLeft_Y', 
                "ThumbLeft_Z":'HandLeft_Z',
                
               'HandRight_X': 'WristRight_X',
               'HandRight_Y': 'WristRight_Y',
               'HandRight_Z': 'WristRight_Z',
               'HandLeft_X': 'WristLeft_X',
               'HandLeft_Y': 'WristLeft_Y',
               'HandLeft_Z': 'WristLeft_Z',
               
               'WristRight_X': 'ElbowRight_X',
               'WristRight_Y': 'ElbowRight_Y',
               'WristRight_Z': 'ElbowRight_Z',
               'WristLeft_X': 'ElbowLeft_X',
               'WristLeft_Y': 'ElbowLeft_Y',
               'WristLeft_Z': 'ElbowLeft_Z',
               
               'ElbowLeft_X': 'ShoulderLeft_X', 
               'ElbowLeft_Y': 'ShoulderLeft_Y', 
               'ElbowLeft_Z': 'ShoulderLeft_Z', 
               'ElbowRight_X': 'ShoulderRight_X',
               'ElbowRight_Y': 'ShoulderRight_Y',
               'ElbowRight_Z': 'ShoulderRight_Z',
               
               'ShoulderRight_X': 'SpineShoulder_X',
               'ShoulderRight_Y': 'SpineShoulder_Y',
               'ShoulderRight_Z': 'SpineShoulder_Z',
               'ShoulderLeft_X': 'SpineShoulder_X',
               'ShoulderLeft_Y': 'SpineShoulder_Y',
               'ShoulderLeft_Z': 'SpineShoulder_Z',
               
               'Neck_X': 'SpineShoulder_X',
               'Neck_Y': 'SpineShoulder_Y',
               'Neck_Z': 'SpineShoulder_Z',
               
               'Head_X': 'Neck_X',
               'Head_Y': 'Neck_Y',
               'Head_Z': 'Neck_Z',
               
               'SpineShoulder_X': 'SpineMid_X',
               'SpineShoulder_Y': 'SpineMid_Y',
               'SpineShoulder_Z': 'SpineMid_Z',
               
               'SpineMid_X': 'SpineBase_X',
               'SpineMid_Y': 'SpineBase_Y',
               'SpineMid_Z': 'SpineBase_Z',
                
               'HipRight_X': 'SpineBase_X',
               'HipRight_Y': 'SpineBase_Y',
               'HipRight_Z': 'SpineBase_Z',
               'HipLeft_X': 'SpineBase_X',
               'HipLeft_Y': 'SpineBase_Y',
               'HipLeft_Z': 'SpineBase_Z',
               
               'KneeRight_X': 'HipRight_X',
               'KneeRight_Y': 'HipRight_Y',
               'KneeRight_Z': 'HipRight_Z',
               'KneeLeft_X': 'HipLeft_X',
               'KneeLeft_Y': 'HipLeft_Y',
               'KneeLeft_Z': 'HipLeft_Z',
               
               'AnkleRight_X': 'KneeRight_X',
               'AnkleRight_Y': 'KneeRight_Y',
               'AnkleRight_Z': 'KneeRight_Z',
               'AnkleLeft_X': 'KneeLeft_X',
               'AnkleLeft_Y': 'KneeLeft_Y',
               'AnkleLeft_Z': 'KneeLeft_Z',
               
               'FootRight_X': 'AnkleRight_X',
               'FootRight_Y': 'AnkleRight_Y',
               'FootRight_Z': 'AnkleRight_Z',
               'FootLeft_X': 'AnkleLeft_X',
               'FootLeft_Y': 'AnkleLeft_Y',
               'FootLeft_Z': 'AnkleLeft_Z'
            }
     }

def getVersion(headers):
    if len(headers) < 95:
        version = 'OLD'
    else:
        version = 'NEW'
    return version


def getHirarchy(headers):
    hirarchyMap= ancestorMap[getVersion(headers)]
    joints = getJoints(headers)
    hirarchy = set()
    for joint, parent in hirarchyMap.items():
        stripedJoint = joint.split('_')[0]
        stripedParent = parent.split('_')[0]
        hirarchy.add((joints.index(stripedJoint), joints.index(stripedParent)))
    print hirarchy
    return hirarchy

def getJoints(headers):
    ver = getVersion(headers)
    map, root = ancestorMap[ver], rootMap[ver]
    s = set()
    s.add(root)
    for header in map.keys():
        s.add(header.split('_')[0])
    return list(s)

def getFileHeader(currentHeader):
    ver = getVersion(currentHeader)
    return headersMap[ver]
    
#Joints = enum(timestamp=0, HipCenter_X=1, HipCenter_Y=2, HipCenter_Z=3, HipCenter_tracked=4, Spine_X=5, Spine_Y=6, Spine_Z=7, Spine_tracked=8, ShoulderCenter_X=9, ShoulderCenter_Y=10, ShoulderCenter_Z=11, ShoulderCenter_tracked=12, Head_X=13, Head_Y=14, Head_Z=15, Head_tracked=16, ShoulderLeft_X=17, ShoulderLeft_Y=18, ShoulderLeft_Z=19, ShoulderLeft_tracked=20, ElbowLeft_X=21, ElbowLeft_Y=22, ElbowLeft_Z=23, ElbowLeft_tracked=24, WristLeft_X=25, WristLeft_Y=26, WristLeft_Z=27, WristLeft_tracked=28, HandLeft_X=29, HandLeft_Y=30, HandLeft_Z=31, HandLeft_tracked=32, ShoulderRight_X=33, ShoulderRight_Y=34, ShoulderRight_Z=35, ShoulderRight_tracked=36, ElbowRight_X=37, ElbowRight_Y=38, ElbowRight_Z=39, ElbowRight_tracked=40, WristRight_X=41, WristRight_Y=42, WristRight_Z=43, WristRight_tracked=44, HandRight_X=45, HandRight_Y=46, HandRight_Z=47, HandRight_tracked=48, HipLeft_X=49, HipLeft_Y=50, HipLeft_Z=51, HipLeft_tracked=52, KneeLeft_X=53, KneeLeft_Y=54, KneeLeft_Z=55, KneeLeft_tracked=56, AnkleLeft_X=57, AnkleLeft_Y=58, AnkleLeft_Z=59, AnkleLeft_tracked=60, FootLeft_X=61, FootLeft_Y=62, FootLeft_Z=63, FootLeft_tracked=64, HipRight_X=65, HipRight_Y=66, HipRight_Z=67, HipRight_tracked=68, KneeRight_X=69, KneeRight_Y=70, KneeRight_Z=71, KneeRight_tracked=72, AnkleRight_X=73, AnkleRight_Y=74, AnkleRight_Z=75, AnkleRight_tracked=76, FootRight_X=77, FootRight_Y=78, FootRight_Z=79, FootRight_tracked=80, FloorPlane_A=81, FloorPlane_B=82, FloorPlane_C=83, FloorPlane_D=84)
Joints = enum(timestamp=0, framenum=1, adc0=2, adc1=3, gyroX=4, gyroY=5, gyroZ=6, 
              HipCenter_X=7, HipCenter_Y=8, HipCenter_Z=9, HipCenter_tracked=10, 
              Spine_X=11, Spine_Y=12, Spine_Z=13, Spine_tracked=14, 
              ShoulderCenter_X=15, ShoulderCenter_Y=16, ShoulderCenter_Z=17, ShoulderCenter_tracked=18, 
              Head_X=19, Head_Y=20, Head_Z=21, Head_tracked=22, 
              ShoulderLeft_X=23, ShoulderLeft_Y=24, ShoulderLeft_Z=25, ShoulderLeft_tracked=26, 
              ElbowLeft_X=27, ElbowLeft_Y=28, ElbowLeft_Z=29, ElbowLeft_tracked=30, 
              WristLeft_X=31, WristLeft_Y=32, WristLeft_Z=33, WristLeft_tracked=34, 
              HandLeft_X=35, HandLeft_Y=36, HandLeft_Z=37, HandLeft_tracked=38, 
              ShoulderRight_X=39, ShoulderRight_Y=40, ShoulderRight_Z=41, ShoulderRight_tracked=42, 
              ElbowRight_X=43, ElbowRight_Y=44, ElbowRight_Z=45, ElbowRight_tracked=46, 
              WristRight_X=47, WristRight_Y=48, WristRight_Z=49, WristRight_tracked=50, 
              HandRight_X=51, HandRight_Y=52, HandRight_Z=53, HandRight_tracked=54, 
              HipLeft_X=55, HipLeft_Y=56, HipLeft_Z=57, HipLeft_tracked=58, 
              KneeLeft_X=59, KneeLeft_Y=60, KneeLeft_Z=61, KneeLeft_tracked=62, 
              AnkleLeft_X=63, AnkleLeft_Y=64, AnkleLeft_Z=65, AnkleLeft_tracked=66, 
              FootLeft_X=67, FootLeft_Y=68, FootLeft_Z=69, FootLeft_tracked=70, 
              HipRight_X=71, HipRight_Y=72, HipRight_Z=73, HipRight_tracked=74, 
              KneeRight_X=75, KneeRight_Y=76, KneeRight_Z=77, KneeRight_tracked=78, 
              AnkleRight_X=79, AnkleRight_Y=80, AnkleRight_Z=81, AnkleRight_tracked=82, 
              FootRight_X=83, FootRight_Y=84, FootRight_Z=85, FootRight_tracked=86, 
              FloorPlane_A=87, FloorPlane_B=88, FloorPlane_C=89, FloorPlane_D=90)
