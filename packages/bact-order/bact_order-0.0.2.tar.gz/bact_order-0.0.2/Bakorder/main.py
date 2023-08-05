def main():

    import os
    import sys
    import subprocess
    import pandas as pd
    import argparse
    from Bio import SeqIO

    def valid_file(file_path):
        if not os.path.isfile(file_path):
            raise argparse.ArgumentTypeError(
                f"{file_path} is not a valid file path")
        if not os.access(file_path, os.R_OK):
            raise argparse.ArgumentTypeError(
                f"{file_path} is not a readable file")
        return file_path

    # Reorder function
    def reorder_genome(start, file, output, header, status):
        starter = int(start)-1
        print(starter, 'should be 1 less than', start)
        for contig_record in SeqIO.parse(open(file), 'fasta'):
            if contig_record.name == header:
                if status:
                    contig = str(contig_record.seq.reverse_complement())
                    starter = (len(contig)-start)-1
                else:
                    contig = str(contig_record.seq)
            str1 = contig[starter:]
            str2 = contig[:starter]
            str_final = '>'+contig_record.id + '\n' + str1 + str2
            with open(output, "w") as out:
                out.write(str_final)

    # Parsing arguments
    default_output = os.path.join(os.getcwd(), 'bakorder_genome.fasta')
    parser = argparse.ArgumentParser(description="Author: J.Iszatt\nPython script to reorder bacterial genomes from bakta output")
    parser.add_argument('-i1', '--tsv', required=True, type=valid_file,  help='Path to the bakta .tsv file')
    parser.add_argument('-i2', '--fna', required=True, type=valid_file,  help='Path to the bakta .fna file')
    parser.add_argument('-o', '--output', default=default_output, help='Direct output to specified file')
    parser.add_argument('--custom_gene', type=str, help='Use a custom string rather than the origin of replication')
    parser.add_argument('--custom_start', type=int, help='Use a custom start point to reorder the genome')
    args = parser.parse_args()

    # Incompatibility warning
    if args.custom_gene and args.custom_start:
        print("These flags may not be used together, choose one or the other")
        sys.exit()

    # Already exists
    if os.path.exists(args.output):
        print(f"{args.output} already exists, exiting")
        sys.exit()

    # Checking input files
    tsv = args.tsv
    if not tsv.endswith('.tsv'):
        print("Invalid tsv file")
        sys.exit()
    fna = args.fna
    if not fna.endswith('.fna'):
        print("Invalid fna file")
        sys.exit()

    # Custom start point
    if args.custom_start:
        print("Running custom start point: reordering")
        reorder_genome(args.custom_start, fna, args.output)

    # Obtaining start point
    df = pd.read_csv(tsv, sep='\t', header=None, comment='#')
    #origins = df[df[7] == 'origin of replication']
    if args.custom_gene:
        origins = df[df[6] == args.custom_gene]
    else:
        origins = df[df[6] == 'dnaA']
    contigs = list(origins[0].unique())

    # Ensuring a single main assembly
    for value in contigs:
        if value.endswith('_1'):
            main = value
            found = True
            break

    if not found:
        print("Main assembly not found, has it got the suffix _1 ?")
        sys.exit()

    # Ensuring a single product and finding strand
    products = []
    for index, row in origins.iterrows():
        if row[0] == main:
            if row[4] == '-':
                products.append([row[4], row[3]]) # [strand,stop] object
            else:
                products.append([row[4], row[2]]) # [strand,start] object

    if len(products) == 1:
        print("Single chromosome, single product found")
        strand = products[0][0]
        start = products[0][1]
    else:
        print("Error")
        sys.exit()

    # Setting reversal status
    if strand == '-':
        reverse = True
    else:
        reverse = False

    # Reordering
    reorder_genome(start, fna, args.output, main, reverse)

if __name__ == '__main__':
    exit(main())
