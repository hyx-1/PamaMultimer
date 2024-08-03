import pymol
from pymol import cmd
def patch_visualization(pdbname, top_patch):
    ## Show pdb structure 
    pymol.cmd.load('./pdb/' + pdbname + '.pdb')
    pymol.cmd.hide('everything')
    #pymol.cmd.color('gray')
    pymol.cmd.bg_color('white')
        
    pymol.cmd.show('surface')
    pymol.cmd.set('transparency',0.6)
    # 获取所有链的列表
    chains = cmd.get_chains()

    # 自定义颜色列表，确保不使用红、绿、蓝
    custom_colors = ["orange", "purple", "cyan", "yellow", "magenta", "gray", "brown", "pink"]

    # 循环遍历链并分配颜色
    for i, chain in enumerate(chains):
        # 如果颜色列表中的颜色用完，则重新从头开始
        color_index = i % len(custom_colors)
        cmd.color(custom_colors[color_index], f"chain {chain}")
    ## Highlight different groups of residues on the structure
    for chain, cluster_ls in top_patch.items():
        #cluster_ls = [[10,15,17,18,20,25,29],[120,125,139,146,117,143,150],[345,333,367,389,400,412,433]]
        color_list = ['red','green','blue']
        
        n = 0
        for ix_ls in cluster_ls:
            sel = '+'.join([str(num) for num in ix_ls])
            #print(sel)
                
            color = color_list[n]
        
            pymol.cmd.select('M'+str(n+1), "chain " +chain + " and resi "+ sel)
            pymol.cmd.show('sticks', 'M'+str(n+1))
            pymol.cmd.color(color, 'M'+str(n+1))
        
            pymol.cmd.label('n. CA and i. '+sel, 'resi')
            pymol.cmd.set('label_size',14)
            pymol.cmd.set('stick_radius',0.5)
                
            n += 1
            
    pymol.cmd.set('stick_transparency',0.2)
    pymol.cmd.save('./result/visualization/' + pdbname + '.pse')
    pymol.cmd.png('./result/visualization/' + pdbname + '.png',width=1200, height=1200, dpi=300, ray=1)    
