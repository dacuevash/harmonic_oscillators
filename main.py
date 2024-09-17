import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore
from oscillators import UDHO, DHO # type: ignore

# Global variables
canvas = None

# Methods
def solve(): # Function called when "Solve!" button is pressed
    global canvas
    time = None
    displacement = None
    
    if eq_selection.get() == "Undamped Oscillator":
        
        # Get data from entries
        mass = float(eval(mass_entry.get()))
        stiffness = float(eval(stiffness_entry.get()))
        rhs = rhs_entry.get()
        x_0 = float(eval(initial_x_entry.get()))
        v_0 = float(eval(initial_v_entry.get()))
        if time_eval_entry.get() != "":
            time = float(eval(time_eval_entry.get()))
        if displacement_eval_entry.get() != "":
            displacement = float(eval(displacement_eval_entry.get()))
        
        # Create oscillator model
        harmonic_oscillator = UDHO(mass, stiffness, x_0, v_0, rhs)
        
        # Update entries according to values
        latex_solution_label.config(image=harmonic_oscillator.get_solution())
        if time != None:
            displacement_eval_result_entry.insert(0, harmonic_oscillator.get_x_at_t(time))
            velocity_eval_result_entry.insert(0, harmonic_oscillator.get_velocity_at_t(time))
        if displacement != None:
            time_eval__result_entry.insert(0, harmonic_oscillator.get_t_at_x(displacement))
        canvas = FigureCanvasTkAgg(master=graphing_frame, figure=harmonic_oscillator.get_graph(0, 5, 100))  # A Tkinter canvas object
        canvas.draw()  # Draw the canvas
        canvas.get_tk_widget().pack(side=tk.TOP, expand=1, padx=10)
    else:
        
        # Get data from entries
        mass = float(eval(mass_entry.get()))
        stiffness = float(eval(stiffness_entry.get()))
        damping = float(eval(damping_entry.get()))
        rhs = rhs_entry.get()
        x_0 = float(eval(initial_x_entry.get()))
        v_0 = float(eval(initial_v_entry.get()))
        if time_eval_entry.get() != "":
            time = float(eval(time_eval_entry.get()))
        if displacement_eval_entry.get() != "":
            displacement = float(eval(displacement_eval_entry.get()))
        
        # Create oscillator model
        harmonic_oscillator = DHO(mass, stiffness, damping, x_0, v_0, rhs)
        
        # Update entries according to values
        latex_solution_label.config(image=harmonic_oscillator.get_solution())
        if time != None:
            displacement_eval_result_entry.insert(0, harmonic_oscillator.get_x_at_t(time))
            velocity_eval_result_entry.insert(0, harmonic_oscillator.get_velocity_at_t(time))
        if displacement != None:
            time_eval__result_entry.insert(0, harmonic_oscillator.get_t_at_x(displacement))
        canvas = FigureCanvasTkAgg(master=graphing_frame, figure=harmonic_oscillator.get_graph(0, 5, 100))  # A Tkinter canvas object
        canvas.draw()  # Draw the canvas
        canvas.get_tk_widget().pack(side=tk.TOP, expand=1, padx=10)

def clear_data():
    # Clear input data
    mass_entry.delete(0, tk.END)
    stiffness_entry.delete(0, tk.END)
    damping_entry.delete(0, tk.END)
    rhs_entry.delete(0, tk.END)
    initial_x_entry.delete(0, tk.END)
    initial_v_entry.delete(0, tk.END)
    time_eval_entry.delete(0, tk.END)
    displacement_eval_entry.delete(0, tk.END)
    # Clear output data
    latex_solution_label.config(image="")
    time_eval__result_entry.delete(0, tk.END)
    displacement_eval_result_entry.delete(0, tk.END)
    velocity_eval_result_entry.delete(0, tk.END)
    global canvas
    if canvas != None:
        canvas.get_tk_widget().destroy()
    

def damping_on_off(*args):
    if eq_selection.get() == "Damped Oscillator":
        damping_label.grid(column=0, row=2)
        damping_entry.grid(column=1, row=2)
    else:
        damping_label.grid_remove()
        damping_entry.grid_remove()
        
def change_eval_var(*args):
    if eval_selection.get() == "Time":
        
        # <-- Input frame --->
        # Add time entry
        time_eval_label.grid(column=0, row=6) 
        time_eval_entry.grid(column=1, row=6)
        # Remove x and x'' entries
        displacement_eval_label.grid_remove()
        displacement_eval_entry.grid_remove()
        velocity_eval_label.grid_remove()
        velocity_eval_entry.grid_remove()
        
        # <-- Output frame --->
        # Add x and x'' entries
        displacement_eval_result_label.grid(column=0, row=1)
        displacement_eval_result_entry.grid(column=1, row=1)
        velocity_eval_result_label.grid(column=0, row=2)
        velocity_eval_result_entry.grid(column=1, row=2)
        # Remove time entry
        time_eval_result_label.grid_remove()
        time_eval__result_entry.grid_remove()
        
    elif eval_selection.get() == "Displacement":
        
        # <-- Input frame --->
        # Add x entry
        displacement_eval_label.grid(column=0, row=6)
        displacement_eval_entry.grid(column=1, row=6)
        # Remove t and x'' entries 
        time_eval_label.grid_remove()
        time_eval_entry.grid_remove()
        velocity_eval_label.grid_remove()
        velocity_eval_entry.grid_remove()
        
        # <-- Output frame --->
        # Add time and velocity entry
        time_eval_result_label.grid(column=0, row=1)
        time_eval__result_entry.grid(column=1, row=1)
        # Remove x entry
        displacement_eval_result_label.grid_remove()
        displacement_eval_result_entry.grid_remove()
        velocity_eval_result_label.grid_remove()
        velocity_eval_result_entry.grid_remove()
        

# <--- GUI Structure --->
# Divide window in three vertical frames
# Frame 1: Oscillator type selection
# Frame 2: Workbench frame
# Frame 3: "Solve!" and "Clear" buttons

# Within frame two, split in two horizontal frames
# Left frame: Data input/output
# Right frame: Graphing space

# Within the left frame, split in two vertical frames
# Upper frame: Input data
# Bottom frame: Output data


# <--- Main window config --->
root = tk.Tk()
root.title("Harmonic Oscillators")
window_width = 1200
window_height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# <--- Equation and evaluation type selection frame START ---> 
selection_frame = tk.Frame(master=root, relief=tk.RAISED, borderwidth=1, height=(0.1*window_height), width=window_width)

label_eq_type_selection = tk.Label(master=selection_frame, text="Select type of oscillator:") # Select equation type 
label_eq_type_selection.grid(column=0, row=0, padx=8, pady=4)
EQ_TYPE_OPTIONS = ['Undamped Oscillator', 'Damped Oscillator']
eq_selection = tk.StringVar(master=selection_frame)
eq_selection.set(EQ_TYPE_OPTIONS[0])
eq_selection.trace_add('write', damping_on_off)
dropdown_menu1 = tk.OptionMenu(selection_frame, eq_selection, *EQ_TYPE_OPTIONS)
dropdown_menu1.grid(column=1, row=0, padx=8, pady=4)

var_eval_type_label = tk.Label(master=selection_frame, text="Choose variable to evaluate:") # Select variable to evaluate
var_eval_type_label.grid(column=0, row=1, padx=8, pady=4)
EVAL_TYPE_OPTIONS = ["Time", "Displacement"]
eval_selection = tk.StringVar(master=selection_frame)
eval_selection.set("Select")
eval_selection.trace_add('write', change_eval_var)
dropdown_menu2 = tk.OptionMenu(selection_frame, eval_selection, *EVAL_TYPE_OPTIONS)
dropdown_menu2.grid(column=1, row=1, padx=8, pady=4)

selection_frame.pack(fill=tk.Y, side=tk.TOP, pady=3)
# <--- Equation and evaluation type selection frame END ---> 


# <--- Workbench frame START --->
workbench_frame = tk.Frame(master=root)

# <-- Data frame START -->
data_frame = tk.Frame(master=workbench_frame)

# <- Input frame START ->
input_frame = tk.Frame(master=data_frame)

mass_label = tk.Label(master=input_frame, text="Enter mass:") # Mass input
mass_label.grid(column=0, row=0)
mass_entry = tk.Entry(master=input_frame)
mass_entry.grid(column=1, row=0)

damping_label = tk.Label(master=input_frame, text="Enter damping:") # Damping input
damping_entry = tk.Entry(master=input_frame)
    
stiffness_label = tk.Label(master=input_frame, text="Enter stiffness:") # Stiffness input
stiffness_label.grid(column=0, row=1)
stiffness_entry = tk.Entry(master=input_frame)
stiffness_entry.grid(column=1, row=1)

initial_x_label = tk.Label(master=input_frame, text="Enter initial position:") # x_0 input
initial_x_label.grid(column=0, row=3)
initial_x_entry = tk.Entry(master=input_frame)
initial_x_entry.grid(column=1, row=3)

initial_v_label = tk.Label(master=input_frame, text="Enter initial velocity:") # v_0 input
initial_v_label.grid(column=0, row=4)
initial_v_entry = tk.Entry(master=input_frame)
initial_v_entry.grid(column=1, row=4)

rhs_label = tk.Label(master=input_frame, text="Enter rhs:") # Either zero or f(t) 
rhs_label.grid(column=0, row=5)
rhs_entry = tk.Entry(master=input_frame)
rhs_entry.grid(column=1, row=5)


time_eval_label = tk.Label(master=input_frame, text="Evaluate at time:") 
time_eval_entry = tk.Entry(master=input_frame)

displacement_eval_label = tk.Label(master=input_frame, text="Evaluate at position:")
displacement_eval_entry = tk.Entry(master=input_frame)

velocity_eval_label = tk.Label(master=input_frame, text="Evaluate at velocity:")
velocity_eval_entry = tk.Entry(master=input_frame)

input_frame.grid(column=0, row=0)

# Create model from data

# <- Input frame END ->

# <- Output frame START ->
output_frame = tk.Frame(master=data_frame)

solution_label = tk.Label(master=output_frame, text="Solution:")
solution_label.grid(column=0, row=0)

latex_solution_label = tk.Label(master=output_frame, image="")
latex_solution_label.grid(column=1, row=0)

time_eval_result_label = tk.Label(master=output_frame, text="Time evaluated at 'x':") 
time_eval__result_entry = tk.Entry(master=output_frame)

displacement_eval_result_label = tk.Label(master=output_frame, text="Position evaluated at 't':")
displacement_eval_result_entry = tk.Entry(master=output_frame)

velocity_eval_result_label = tk.Label(master=output_frame, text="Velocity evaluated at 't':")
velocity_eval_result_entry = tk.Entry(master=output_frame)

output_frame.grid(column=0, row=1) # Output frame ends here
# <- Output frame END ->

data_frame.grid(column=0, row=0)
# <-- Data frame END -->

# <-- Graphing frame START -->
graphing_frame = tk.Frame(master=workbench_frame)

graphing_frame.grid(column=1, row=0)
# <-- Graphing frame END -->

workbench_frame.pack(fill=tk.Y, pady=3)
# <--- Workbench frame END --->

# <--- Solving buttons frame START --->
solving_buttons_frame = tk.Frame(master=root)

solve_button = tk.Button(master=solving_buttons_frame, text="Solve!", command=solve)
solve_button.pack(pady=10)

clear_button = tk.Button(master=solving_buttons_frame, text="Clear all data", command=clear_data)
clear_button.pack(pady=10)

solving_buttons_frame.pack(fill=tk.Y, pady=3)
# <---- Solving buttons frame END --->

root.mainloop()
