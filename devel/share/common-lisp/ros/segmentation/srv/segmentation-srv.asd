
(cl:in-package :asdf)

(defsystem "segmentation-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :segmentation-msg
)
  :components ((:file "_package")
    (:file "Segmentation" :depends-on ("_package_Segmentation"))
    (:file "_package_Segmentation" :depends-on ("_package"))
  ))