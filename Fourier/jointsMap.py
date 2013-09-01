def enum(**enums):
    return type('Enum', (), enums)
Joints = enum(timestamp=0, HipCenter_X=1, HipCenter_Y=2, HipCenter_Z=3, HipCenter_tracked=4, Spine_X=5, Spine_Y=6, Spine_Z=7, Spine_tracked=8, ShoulderCenter_X=9, ShoulderCenter_Y=10, ShoulderCenter_Z=11, ShoulderCenter_tracked=12, Head_X=13, Head_Y=14, Head_Z=15, Head_tracked=16, ShoulderLeft_X=17, ShoulderLeft_Y=18, ShoulderLeft_Z=19, ShoulderLeft_tracked=20, ElbowLeft_X=21, ElbowLeft_Y=22, ElbowLeft_Z=23, ElbowLeft_tracked=24, WristLeft_X=25, WristLeft_Y=26, WristLeft_Z=27, WristLeft_tracked=28, HandLeft_X=29, HandLeft_Y=30, HandLeft_Z=31, HandLeft_tracked=32, ShoulderRight_X=33, ShoulderRight_Y=34, ShoulderRight_Z=35, ShoulderRight_tracked=36, ElbowRight_X=37, ElbowRight_Y=38, ElbowRight_Z=39, ElbowRight_tracked=40, WristRight_X=41, WristRight_Y=42, WristRight_Z=43, WristRight_tracked=44, HandRight_X=45, HandRight_Y=46, HandRight_Z=47, HandRight_tracked=48, HipLeft_X=49, HipLeft_Y=50, HipLeft_Z=51, HipLeft_tracked=52, KneeLeft_X=53, KneeLeft_Y=54, KneeLeft_Z=55, KneeLeft_tracked=56, AnkleLeft_X=57, AnkleLeft_Y=58, AnkleLeft_Z=59, AnkleLeft_tracked=60, FootLeft_X=61, FootLeft_Y=62, FootLeft_Z=63, FootLeft_tracked=64, HipRight_X=65, HipRight_Y=66, HipRight_Z=67, HipRight_tracked=68, KneeRight_X=69, KneeRight_Y=70, KneeRight_Z=71, KneeRight_tracked=72, AnkleRight_X=73, AnkleRight_Y=74, AnkleRight_Z=75, AnkleRight_tracked=76, FootRight_X=77, FootRight_Y=78, FootRight_Z=79, FootRight_tracked=80, FloorPlane_A=81, FloorPlane_B=82, FloorPlane_C=83, FloorPlane_D=84)
ancestorMap = {Joints.ElbowLeft_X: Joints.ShoulderLeft_X, 
               Joints.ElbowLeft_Y: Joints.ShoulderLeft_Y, 
               Joints.ElbowLeft_Z: Joints.ShoulderLeft_Z, 
               Joints.ElbowRight_X: Joints.ShoulderRight_X,
               Joints.ElbowRight_Y: Joints.ShoulderRight_Y,
               Joints.ElbowRight_Z: Joints.ShoulderRight_Z,
               Joints.KneeRight_X: Joints.HipRight_X,
               Joints.KneeRight_Y: Joints.HipRight_Y,
               Joints.KneeRight_Z: Joints.HipRight_Z,
               Joints.KneeLeft_X: Joints.HipLeft_X,
               Joints.KneeLeft_Y: Joints.HipLeft_Y,
               Joints.KneeLeft_Z: Joints.HipLeft_Z,
               Joints.WristRight_X: Joints.ElbowRight_X,
               Joints.WristRight_Y: Joints.ElbowRight_Y,
               Joints.WristRight_Z: Joints.ElbowRight_Z,
               Joints.WristLeft_X: Joints.ElbowLeft_X,
               Joints.WristLeft_Y: Joints.ElbowLeft_Y,
               Joints.WristLeft_Z: Joints.ElbowLeft_Z}