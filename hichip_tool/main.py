#########################################
# Author: Chenfu Shi
# Email: chenfu.shi@postgrad.manchester.ac.uk


# Main executor of the pipeline to call peaks from hicpro data

#########################################


def main():
    import os
    import argparse
    ## here all inputs.


    parser = argparse.ArgumentParser(description="Peak calling from HiChIP data")

    parser.add_argument("-i", "--input", dest="hicpro_results",action="store",required=True,
                        help="HiC-Pro results directory containing validPairs file and others")
    parser.add_argument("-o", "--output", dest="output_directory",action="store",required=True,
                        help="Output file, will write temporary files in that directory")
    parser.add_argument("-r", "--resfrag", dest="resfrag",action="store",required=True,
                        help="HiCpro resfrag file")
    parser.add_argument("-f", "--FDR", dest="FDR",action="store",required=False, default=0.01, type=float,
                        help="False discovery rate, default = 0.01")                        
    parser.add_argument("-a", "--annotation", dest="sizes",action="store",required=False, default=None,
                        help="HiCpro chromosome annotation file, default uses human chromosomes, excludes chrY")
    parser.add_argument("-t", "--temporary_loc", dest="temporary_loc",action="store",required=False, default=None,
                        help="Temporary directory. If not supplied will be output directory")
    parser.add_argument("-w", "--worker_threads", dest="threads",action="store",required=False, default=4, type=int,
                        help="Number of threads, minimum 4")
    parser.add_argument("-k", "--keep_temp", dest="keeptemp",action="store_true", default=False,
                        help="Keep temporary files")
    args = parser.parse_args()





    hicpro_results = os.path.abspath(args.hicpro_results)
    resfrag = os.path.abspath(args.resfrag)
    sizes = args.sizes
    if args.temporary_loc == None:
        temporary_loc = os.path.abspath(args.output_directory)
    else:
        temporary_loc = os.path.abspath(args.temporary_loc)
    output_dir = os.path.abspath(args.output_directory)
    keeptemp = args.keeptemp
    threads=args.threads
    FDR=args.FDR
    os.environ["OMP_NUM_THREADS"] = threads
    os.environ["OPENBLAS_NUM_THREADS"] = threads
    os.environ["MKL_NUM_THREADS"] = threads
    os.environ["VECLIB_MAXIMUM_THREADS"] = threads
    os.environ["NUMEXPR_NUM_THREADS"] = threads

    print("Info: \n HiC-Pro data folder: {} \n Restriction fragment file: {} \n Chromosome annotation file: {} \n Temporary location: {}".format(hicpro_results,resfrag,sizes,temporary_loc))
    print(" FDR: {}".format(FDR))
    print(" Output directory: {} \n Keep temporary files?: {} \n Threads(minimum is 4): {}".format(output_dir,keeptemp,threads))
    

    #apparently moving this should make sure that number of threads is respected in numpy?
    try:
        #this works only when installed
        from hichip_tool import interaction_to_sparse,sparse_to_peaks
    except:
        import interaction_to_sparse 
        import sparse_to_peaks
    
    CSR_mat,frag_index,frag_prop,frag_amount,valid_chroms,chroms_offsets = interaction_to_sparse.HiCpro_to_sparse(hicpro_results,resfrag,sizes,temporary_loc,keeptemp=keeptemp)


    smoothed_diagonal , refined_peaks = sparse_to_peaks.sparse_to_peaks(CSR_mat,frag_index,frag_prop,frag_amount,valid_chroms,chroms_offsets,output_dir,FDR=FDR,threads=threads,keeptemp=keeptemp)


    #do ip efficiency










if __name__=="__main__":
    main()