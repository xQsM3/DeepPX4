
(cl:in-package :asdf)

(defsystem "segmentation-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "SegImage" :depends-on ("_package_SegImage"))
    (:file "_package_SegImage" :depends-on ("_package"))
    (:file "SegImage" :depends-on ("_package_SegImage"))
    (:file "_package_SegImage" :depends-on ("_package"))
  ))