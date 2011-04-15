$(function() {
jQuery(".vDateTimeField").datetimepicker({ 
  dateFormat: 'yy-mm-dd',
  hourGrid: 6,
  minuteGrid: 15,
  timeText: "时间",
  hourText:  "时",
  minuteText:  "分",
  secondText:  "秒",
  currentText:  "现在",
  closeText:  "完成",   
  });
jQuery(".vTimeField").timepicker({ 
  hourGrid: 6,
  minuteGrid: 15,
  timeText: "时间",
  hourText:  "时",
  minuteText:  "分",
  secondText:  "秒",
  currentText:  "现在",
  closeText:  "完成",      
  });
});