import sys


class GlowingBacteria:
    
    def __init__(self):
        self.keys = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        self.orig_plasm = self.compl_plasm = self.orig_gfp = self.compl_gfp = ''
        self.site_r = self.site_l = self.compl_site_r = self.compl_site_l = ''
        self.double_strand = ''
        self.file_content = []

    def read_file(self):
        file_name = input()
        # args = sys.argv
        # file_name = args[1]
        # print(file_name)
        
        with open(file_name, 'r') as f:
            for line in f:
                self.file_content.append(line)
        
    def get_data(self):
        self.orig_plasm = self.file_content[0].strip('\n')
        self.compl_plasm = self.replacing(self.orig_plasm)
        self.orig_gfp = self.file_content[2].strip('\n')
        self.site_l, self.site_r = self.file_content[3].strip('\n').split()
        
    def cut_plasm(self):
        restr_site1 = self.file_content[1].strip('\n')
        i1 = self.orig_plasm.find(restr_site1) + 1
        first_strand = self.orig_plasm[:i1] + ' ' + self.orig_plasm[i1:]
        restr_site2 = self.replacing(restr_site1)
        i2 = self.compl_plasm.rfind(restr_site2) + len(restr_site2) - 1
        second_strand = self.compl_plasm[:i2] + ' ' + self.compl_plasm[i2:]
        return f"{first_strand}\n{second_strand}"
        
    def replacing(self, strand):
        strand_list = list(strand)
        replaced_strand = []
        for i in strand_list:
            x = self.keys[i]
            replaced_strand.append(x)
        return ''.join(replaced_strand)
    
    @staticmethod
    def cut_orig_gfp(strand, site_1, site_2):
        i1 = strand.find(site_1) + 1
        first_strand = strand[i1:]
        i2 = first_strand.rfind(site_2) + 1
        final_strand = first_strand[:i2]
        return final_strand
    
    @staticmethod
    def cut_compl_gfp(strand, site_1, site_2):
        i1 = strand.find(site_1) + len(site_1) - 1
        first_strand = strand[i1:]
        i2 = first_strand.rfind(site_2) + len(site_2) - 1
        final_strand = first_strand[:i2]
        return final_strand
        
    def convert_compl_gfp(self):
        self.compl_gfp = self.replacing(self.orig_gfp)
        self.compl_site_l = self.replacing(self.site_l)
        self.compl_site_r = self.replacing(self.site_r)
        
    def gluing(self):
        plasmid = self.cut_plasm().strip('\n').split()
        self.convert_compl_gfp()
        gfp_1 = self.cut_orig_gfp(self.orig_gfp, self.site_l, self.site_r).strip('\n')
        gfp_2 = self.cut_compl_gfp(self.compl_gfp, self.compl_site_l, self.compl_site_r)
        line_1 = f"{plasmid[0]}{gfp_1}{plasmid[1]}"
        line_2 = f"{plasmid[2]}{gfp_2}{plasmid[3]}"
        self.double_strand = f"{line_1}\n{line_2}"
        print(self.double_strand)

    def main(self):
        self.read_file()
        self.get_data()
        self.gluing()
        
        
if __name__ == '__main__':
    GlowingBacteria().main()
