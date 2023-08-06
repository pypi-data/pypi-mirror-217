import sys
import argparse
from pctk import plot
from pctk import render
from pctk import config




def main(): 
    parser = argparse.ArgumentParser(description="PhysiCell Tool Kit for handling and processing Physicell outputs")
    subparser = parser.add_subparsers(dest='command', help='sub-command help')
    
    plot_parser = subparser.add_parser('plot-time-course',
                                        description="Plot total cell grouped as Alive/Necrotic/Apoptotic vs Time")
    plot_parser.add_argument("output_folder", action="store", help="Folder where the simulation output is stored")
    plot_parser.add_argument("--format", action="store", dest="format", choices=("physicell", "physiboss"),
                        help="Format of the input data", default="physicell")
    plot_parser.add_argument("--figout", action="store", dest="fig_fname", default="./cell_vs_time.png",
                        help="File name to save the plot")    
    plot_parser.add_argument("--csvout", action="store", dest="csv_fname", default=None,
                        help="File name to store the summary table used for the plot")


    pov_parser = subparser.add_parser('povray')
    pov_parser.add_argument("--config", action="store", help="XML configuration file for creating pov files")
    pov_parser.add_argument("--format", action="store", dest="format", choices=("physicell", "physiboss"),
                        help="Format of the input data", default="physicell")
    pov_parser.add_argument("--render",  action='store_true',
                        help="Render the .pov files into .png. Requires povray ({povray_link})")
    pov_parser.add_argument("--width", action="store", dest="width", type=int, default=2160, 
                        help="Width for povray rendered image")
    pov_parser.add_argument("--height", action="store", dest="height", type=int, default=2160, 
                        help="Heigh for povray rendered image")
    pov_parser.add_argument("--cpus", action="store", dest="cpus", type=int, default=4, 
                        help="Total cpus availabile to run in parallel using multiprocessing")
    pov_parser.add_argument("--create-config", action="store", dest="config_out", default="",
                                help="Create a defaul config XML file for generating POV files")
    pov_parser.add_argument("--idxs", action="store", dest="strn_idxs", default="",
                        help="String specifing the indexes of the output files. \
                            The supported options include: \
                            - slices: 1:10:1\
                            - indexes: 1,2,5,10\
                            - all (use glob)")
    

    args = parser.parse_args()
    if args.command == "plot-time-course":
        plot.plot_time_course(args.output_folder, fig_fname=args.fig_fname, csv_fname=args.csv_fname, format=args.format)
    elif args.command == "povray":
        if args.config_out:
            with open(args.config_out, "w") as fh:
                print(f"Writing default POV-write config into {args.config_out}.")
                fh.writelines(config.DEFAULT_XML)
        else:
            if args.config:
                render.write_pov_files(args)
            else:
                print("Error: --config is required parameter")
                pov_parser.print_help()
    else:
        parser.parse_args(["--help"])
        sys.exit(0)