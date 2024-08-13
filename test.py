import pyscreenshot 
  
# To capture the screen 
image = pyscreenshot.grab(childprocess=False) 
  
# To display the captured screenshot 
image.show() 
  
# To save the screenshot 
image.save("GeeksforGeeks.png") 