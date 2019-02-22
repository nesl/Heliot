\* placethings *\
Minimize
OBJ: LongestPathLength
Subject To
_C1: X_task_findObject_P3_2XLARGE.0 + X_task_findObject_T2_MICRO.0
 + X_task_findObject_T3_LARGE.0 = 1
_C10:
 2 XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 <= 0
_C11: XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 >= 0
_C12: 2 XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 <= 1
_C13: XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 >= 0
_C14: 2 XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 <= 1
_C15: XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'CONTROLLER.0')
 >= 0
_C16: 2 XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'CONTROLLER.0')
 <= 1
_C17: XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 >= 0
_C18: 2 XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 <= 1
_C19: XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 >= -1
_C2: X_task_findObject_P3_2XLARGE.0 + X_task_findObject_T2_MICRO.0
 + X_task_findObject_T3_LARGE.0 = 1
_C20: 2 XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 <= 0
_C21: XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CAMERA.0')
 >= -1
_C22: 2 XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CAMERA.0')
 <= 0
_C23: XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CONTROLLER.0')
 >= -1
_C24:
 2 XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CONTROLLER.0')
 <= 0
_C25: XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 >= -1
_C26:
 2 XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 <= 0
_C27: XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 >= -1
_C28:
 2 XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 <= 0
_C29: XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'CAMERA.0')
 >= -1
_C3: XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CAMERA.0')
 >= -1
_C30: 2 XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'CAMERA.0')
 <= 0
_C31: XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 >= -1
_C32:
 2 XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 <= 0
_C33:
 XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 >= -1
_C34:
 2 XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 <= 0
_C35: XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 >= -1
_C36:
 2 XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T3_LARGE.0')
 - X_task_findObject_T3_LARGE.0 <= 0
_C37: XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CAMERA.0')
 >= -1
_C38: 2 XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CAMERA.0')
 <= 0
_C39: XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 >= -1
_C4: 2 XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CAMERA.0')
 <= 0
_C40:
 2 XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 <= 0
_C41:
 XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
 >= -1
_C42:
 2 XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
 <= 0
_C43: XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CAMERA.0')
 - X_task_findObject_T3_LARGE.0 >= -1
_C44: 2 XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CAMERA.0')
 - X_task_findObject_T3_LARGE.0 <= 0
_C45: XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'T2_MICRO.0')
 - X_task_findObject_T3_LARGE.0 >= -1
_C46: 2 XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'T2_MICRO.0')
 - X_task_findObject_T3_LARGE.0 <= 0
_C47: XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 - X_task_findObject_T3_LARGE.0 >= 0
_C48:
 2 XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 - X_task_findObject_T3_LARGE.0 <= 1
_C49: XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'P3_2XLARGE.0')
 - X_task_findObject_T3_LARGE.0 >= -1
_C5: XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 >= -1
_C50:
 2 XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'P3_2XLARGE.0')
 - X_task_findObject_T3_LARGE.0 <= 0
_C51: XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T3_LARGE.0')
 >= -1
_C52: 2 XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T3_LARGE.0')
 <= 0
_C53: XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T2_MICRO.0')
 >= -1
_C54: 2 XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T2_MICRO.0')
 <= 0
_C55: XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'CONTROLLER.0')
 >= 0
_C56: 2 XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'CONTROLLER.0')
 <= 1
_C57: XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'P3_2XLARGE.0')
 >= -1
_C58: 2 XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'P3_2XLARGE.0')
 <= 0
_C59: XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'T3_LARGE.0')
 - X_task_findObject_T2_MICRO.0 >= -1
_C6: 2 XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
 - X_task_findObject_T2_MICRO.0 <= 0
_C60: 2 XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'T3_LARGE.0')
 - X_task_findObject_T2_MICRO.0 <= 0
_C61: XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CAMERA.0')
 - X_task_findObject_T2_MICRO.0 >= -1
_C62: 2 XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CAMERA.0')
 - X_task_findObject_T2_MICRO.0 <= 0
_C63: XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CONTROLLER.0')
 - X_task_findObject_T2_MICRO.0 >= 0
_C64:
 2 XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CONTROLLER.0')
 - X_task_findObject_T2_MICRO.0 <= 1
_C65: XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'P3_2XLARGE.0')
 - X_task_findObject_T2_MICRO.0 >= -1
_C66:
 2 XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'P3_2XLARGE.0')
 - X_task_findObject_T2_MICRO.0 <= 0
_C67: XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T3_LARGE.0')
 >= -1
_C68:
 2 XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T3_LARGE.0')
 <= 0
_C69: XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'CAMERA.0')
 >= -1
_C7: XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
 >= -1
_C70: 2 XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'CAMERA.0')
 <= 0
_C71: XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T2_MICRO.0')
 >= -1
_C72:
 2 XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T2_MICRO.0')
 <= 0
_C73:
 XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'P3_2XLARGE.0')
 >= -1
_C74:
 2 XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'P3_2XLARGE.0')
 <= 0
_C75: XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T3_LARGE.0')
 - X_task_findObject_P3_2XLARGE.0 >= -1
_C76:
 2 XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T3_LARGE.0')
 - X_task_findObject_P3_2XLARGE.0 <= 0
_C77: XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CAMERA.0')
 - X_task_findObject_P3_2XLARGE.0 >= -1
_C78: 2 XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CAMERA.0')
 - X_task_findObject_P3_2XLARGE.0 <= 0
_C79: XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T2_MICRO.0')
 - X_task_findObject_P3_2XLARGE.0 >= -1
_C8:
 2 XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
 <= 0
_C80:
 2 XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T2_MICRO.0')
 - X_task_findObject_P3_2XLARGE.0 <= 0
_C81:
 XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 - X_task_findObject_P3_2XLARGE.0 >= 0
_C82:
 2 XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 - X_task_findObject_P3_2XLARGE.0 <= 1
_C83: XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'CONTROLLER.0')
 + XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 + XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T2_MICRO.0')
 + XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T3_LARGE.0')
 + XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'CAMERA.0')
 + XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 + XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T2_MICRO.0')
 + XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T3_LARGE.0')
 + XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CAMERA.0')
 + XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
 + XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
 + XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T3_LARGE.0')
 + XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CAMERA.0')
 + XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CONTROLLER.0')
 + XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 + XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'T3_LARGE.0')
 + XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CAMERA.0')
 + XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
 + XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 + XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
 + XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'CONTROLLER.0')
 + XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'P3_2XLARGE.0')
 + XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T2_MICRO.0')
 + XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T3_LARGE.0')
 + XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'CAMERA.0')
 + XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'P3_2XLARGE.0')
 + XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T2_MICRO.0')
 + XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T3_LARGE.0')
 + XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CAMERA.0')
 + XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 + XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T2_MICRO.0')
 + XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T3_LARGE.0')
 + XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CAMERA.0')
 + XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CONTROLLER.0')
 + XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'P3_2XLARGE.0')
 + XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'T3_LARGE.0')
 + XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CAMERA.0')
 + XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 + XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'P3_2XLARGE.0')
 + XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'T2_MICRO.0') = 2
_C84: LongestPathLength
 - 66 XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T3_LARGE.0')
 - 10 XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 - 884 X_task_findObject_T3_LARGE.0 >= 0
_C85: LongestPathLength
 - 68 XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T2_MICRO.0')
 - 12 XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CONTROLLER.0')
 - 2400 X_task_findObject_T2_MICRO.0 >= 0
_C86: LongestPathLength
 - 64 XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - 8 XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CONTROLLER.0')
 - 100 X_task_findObject_P3_2XLARGE.0 >= 0
_C87: 251658240 X_task_findObject_T3_LARGE.0 <= 1.40737488355e+14
_C88: 8589934592 X_task_findObject_T3_LARGE.0 <= 68719476736
_C89: 60 X_task_findObject_T3_LARGE.0 <= 100
_C9: XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'P3_2XLARGE.0')
 - X_task_findObject_P3_2XLARGE.0 >= -1
_C90: 251658240 X_task_findObject_T2_MICRO.0 <= 257698037760
_C91: 8589934592 X_task_findObject_T2_MICRO.0 <= 8589934592
_C92: 60 X_task_findObject_T2_MICRO.0 <= 100
_C93: 251658240 X_task_findObject_P3_2XLARGE.0 <= 1.40737488355e+14
_C94: 34359738368 X_task_findObject_P3_2XLARGE.0 <= 137438953472
_C95: 5 X_task_findObject_P3_2XLARGE.0 <= 100
_C96: 60 X_task_findObject_P3_2XLARGE.0 <= 100
Bounds
0 <= LongestPathLength <= 2147483647
Binaries
XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'CONTROLLER.0')
XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'P3_2XLARGE.0')
XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T2_MICRO.0')
XX_(u'task_camera',_u'CAMERA.0')_(u'task_findObject',_u'T3_LARGE.0')
XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'CAMERA.0')
XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'P3_2XLARGE.0')
XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T2_MICRO.0')
XX_(u'task_camera',_u'CONTROLLER.0')_(u'task_findObject',_u'T3_LARGE.0')
XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CAMERA.0')
XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
XX_(u'task_camera',_u'P3_2XLARGE.0')_(u'task_findObject',_u'T3_LARGE.0')
XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CAMERA.0')
XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'CONTROLLER.0')
XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'P3_2XLARGE.0')
XX_(u'task_camera',_u'T2_MICRO.0')_(u'task_findObject',_u'T3_LARGE.0')
XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CAMERA.0')
XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'CONTROLLER.0')
XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'P3_2XLARGE.0')
XX_(u'task_camera',_u'T3_LARGE.0')_(u'task_findObject',_u'T2_MICRO.0')
XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'CONTROLLER.0')
XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'P3_2XLARGE.0')
XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T2_MICRO.0')
XX_(u'task_findObject',_u'CAMERA.0')_(u'task_alert',_u'T3_LARGE.0')
XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'CAMERA.0')
XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'P3_2XLARGE.0')
XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T2_MICRO.0')
XX_(u'task_findObject',_u'CONTROLLER.0')_(u'task_alert',_u'T3_LARGE.0')
XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CAMERA.0')
XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'CONTROLLER.0')
XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T2_MICRO.0')
XX_(u'task_findObject',_u'P3_2XLARGE.0')_(u'task_alert',_u'T3_LARGE.0')
XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CAMERA.0')
XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'CONTROLLER.0')
XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'P3_2XLARGE.0')
XX_(u'task_findObject',_u'T2_MICRO.0')_(u'task_alert',_u'T3_LARGE.0')
XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CAMERA.0')
XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'CONTROLLER.0')
XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'P3_2XLARGE.0')
XX_(u'task_findObject',_u'T3_LARGE.0')_(u'task_alert',_u'T2_MICRO.0')
X_task_findObject_P3_2XLARGE.0
X_task_findObject_T2_MICRO.0
X_task_findObject_T3_LARGE.0
End
