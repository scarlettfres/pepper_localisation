#!/usr/bin/env python
import roslib
import rospy
from sensor_msgs.msg import JointState
import tf
from naoqi import ALProxy
import geometry_msgs.msg
from tf.msg import tfMessage
import sys
from tf.transformations import (quaternion_inverse,
                                quaternion_conjugate,
                                quaternion_from_euler)

"""
when launching pepper, odom is the begining of the tf tree. We want
our frame "map" ( which is initalized by a mark) to be the origin of the frame.
Base_link would have the parent odom, and the parent mark. It is not possible
so we have to invert the parent and child between base_link and odom to
modify the t tree as we want
"""


class publish_odom:

    """
    contains all services that can be called by the client
    """

    def __init__(self, ip):
        self.motionProxy = ALProxy("ALMotion", ip, 9559)
        self.broadcaster = tf.TransformBroadcaster()
        rospy.Subscriber("/joint_states", JointState, self.callback)

    def callback(self, data):

        position = self.motionProxy.getPosition("Torso", 1, True)

        # trans = [data.transforms[0].transform.translation.x,
        #          data.transforms[0].transform.translation.y,
        #          data.transforms[0].transform.translation.z]
        # rot = [data.transforms[0].transform.rotation.x,
        #        data.transforms[0].transform.rotation.y,
        #        data.transforms[0].transform.rotation.z,
        #        data.transforms[0].transform.rotation.w
        #        ]

        # euler = euler_from_quaternion(rot)
        trans = (position[0], position[1], position[2])
        rot = quaternion_from_euler(position[3], position[4], position[5])

        # rot_bis = quaternion_conjugate(rot)
        self.broadcaster.sendTransform(trans, rot, rospy.Time.now(),
                                       "/odom_bis",
                                       "/base_link")

if __name__ == '__main__':
    rospy.init_node('invert_tf_odom_parent')
    publish_odom(sys.argv[1])
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
        # mon_fichier_speed.close()

        print "Finished."
