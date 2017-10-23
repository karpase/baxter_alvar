#!/usr/bin/python2

import rospy

import ar_track_alvar_msgs.msg
import tf
import numpy as np

class AlvarToTFProcessor:
    def __init__(self):
        self.baxter_marker_id = 1
        self.baxter_display = "display"        
        self.alpha = 0.1

        self.br = tf.TransformBroadcaster()
        self.bl = tf.TransformerROS()

        self.translation_avg = np.array([0,0,0])
        self.rotation_avg = np.array([0, 0, 0, 1])
        

    def start(self):
        rospy.Subscriber("/ar_pose_marker",ar_track_alvar_msgs.msg.AlvarMarkers, self.callback)

    def callback(self, msg):
        for m in msg.markers:
            if m.id == self.baxter_marker_id:
                self.translation_avg = self.translation_avg * (1 - self.alpha) + np.array([m.pose.pose.position.x, m.pose.pose.position.y, m.pose.pose.position.z]) * self.alpha

                self.rotation_avg = tf.transformations.quaternion_slerp(self.rotation_avg, 
			np.array([m.pose.pose.orientation.x, m.pose.pose.orientation.y, m.pose.pose.orientation.z, m.pose.pose.orientation.w]), self.alpha)

                cam_to_marker_matrix = self.bl.fromTranslationRotation(self.translation_avg, self.rotation_avg)

                print m

                marker_to_cam_matrix = tf.transformations.inverse_matrix(cam_to_marker_matrix)

                self.br.sendTransform(
                   tf.transformations.translation_from_matrix(marker_to_cam_matrix),
                   tf.transformations.quaternion_from_matrix(marker_to_cam_matrix),
                   msg.header.stamp,
                   m.header.frame_id,
                   self.baxter_display)

               	    


def main():
    rospy.init_node('process_alvar_to_tf')

    x = AlvarToTFProcessor()
    x.start()

    rospy.spin()

if __name__ == '__main__':
    main()
