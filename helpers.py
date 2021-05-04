def change_color(widget):
    '''
    Creates illusion of widget "blinking" by gradually switching colors to background color and back to original widget text color.
    
    NOTE1: running .after() in a loop (e.g. for) does not work, as the loop runs while after-round is still waiting
    NOTE2: subsequent .after()-calls, need to have increasing delays, as the first after-call delay time nis substracted from the 2nd one, the 2nd from the 3rd etc.
    --> solutions:
        1) extend tint-list by how often should be ran through
        2) call .enumerate() and multiply the enumerator by the desired time for each color
    '''
    def _color_text(widget, color):
        ''' Change font color of widget to "color" '''
        widget.config(fg=color)

    tints_of_blue = ["#0000FF", "#1919ff", "#3232ff", "#4c4cff", "#6666ff", "#7f7fff", "#9999ff", "#b2b2ff", "#ccccff", "#e5e5ff"]  #list of blue with decreasing saturation
    tints_of_blue += tints_of_blue[::-1]  #append reversed list to list
    tints_of_blue *= 3
    time_per_col = int(4000/len(tints_of_blue))   #each "blink" should take 60 seconds

    for n, tint in enumerate(tints_of_blue):
        widget_after_id = widget.after(time_per_col*n, _color_text, widget, tint)
        RECORD_BUTTON_BLINK[widget] = widget_after_id


 
global RECORD_BUTTON_BLINK  #initiate dict that stores after_ids and cancels id for current widget if it is still running
RECORD_BUTTON_BLINK = {}

def changeOnHover(button, fgColorOnHover, fgColorOnLeave, bgColorOnHover="#DCDAD5", bgColorOnLeave="#DCDAD5"): 
    def _modify(e, fgcol, bgcol, blink=0):
        if button in RECORD_BUTTON_BLINK.keys(): 
            button.after_cancel(RECORD_BUTTON_BLINK[button])  #if previous after still running for this widget - cancel it, so that blinking frequency is not changed
        
        if (blink != 0) and ('CLICK ME!' in button.cget('text')):  #tun only if blink is set to one and if button text does not contain 'HIT ME!' substring"
            change_color(button)
        button.config(fg=fgcol)
        button.config(bg=bgcol)
    
    # background on cursor entering widget 
    button.bind("<Enter>", 
                func=lambda e, fgcol=fgColorOnHover, bgcol=bgColorOnHover, blink=1: _modify(e, fgcol, bgcol, blink)
                )  
        
    # background color on cursor leaving widget 
    button.bind("<Leave>", 
                func=lambda e, fgcol=fgColorOnLeave, bgcol=bgColorOnLeave: _modify(e, fgcol, bgcol)
                )  