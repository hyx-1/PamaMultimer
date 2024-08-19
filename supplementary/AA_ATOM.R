library(ggplot2)
library(patchwork)
library(RColorBrewer)
library(ggsci)
library(ggpubr)
AA_virus = read.table("AA_virus.txt")
AA_all = read.table("AA.txt")
AA_truecore = read.table("AA_truecore.txt")
#AA = rbind(AA_all,AA_virus,AA_truecore)
ATOM_virus = read.table("ATOM_virus.txt")
ATOM_all = read.table("ATOM.txt")
ATOM_truecore = read.table("ATOM_truecore.txt")
#ATOM = rbind(ATOM_all,ATOM_virus,ATOM_truecore)
numbers = rbind(AA_all*10,ATOM_all,AA_virus*10,ATOM_virus,AA_truecore*10,ATOM_truecore)
type1 = rep("The whole",times=length(AA_all$V1)*2)
type2 = rep("Riboviria",times=length(AA_virus$V1)*2)
type3 = rep("Eukaryotic",times=length(AA_truecore$V1)*2)
type=cbind(t(type1),t(type2),t(type3))
AA_or_ATOM = cbind(t(rep("AA*10",times = length(AA_all$V1))),
t(rep("ATOM",times = length(AA_all$V1))),
t(rep("AA*10",times = length(AA_virus$V1))),
t(rep("ATOM",times = length(AA_virus$V1))),
t(rep("AA*10",times = length(AA_truecore$V1))),
t(rep("ATOM",times = length(AA_truecore$V1))))
data = data.frame(Numbers = numbers$V1,data_type = t(type), AA_or_ATOM = t(AA_or_ATOM))

data %>% {
  p <- ggplot(.,mapping = aes(AA_or_ATOM,Numbers,fill = data_type))
  p1 <- p + geom_boxplot()+
            stat_compare_means()+
            scale_fill_lancet()+
            theme_bw()+
            theme(legend.position = "none")+
            #scale_y_continuous(limits = c(0,20000),
             #        breaks = seq(0,20000,1000),
              #       sec.axis = sec_axis(~./10,
               #                          name = 'Test positive rate',
                #                         breaks = seq(0,2000,100)))+
theme_classic()
  #p2 <- p + geom_boxplot(notch = T)+
    #        scale_fill_lancet()+
   #         theme_classic()
  #p1 + p2
p1
}
ggsave("AA_and_ATOM.jpg")
mtcars %>% {
  p <- ggplot(.,mapping = aes(as.factor(am),mpg,fill = as.factor(cyl)))
  p1 <- p + geom_boxplot()+
            stat_compare_means()+
            scale_fill_lancet()+
            theme_bw()+
            theme(legend.position = "none")+
theme_classic()
  #p2 <- p + geom_boxplot(notch = T)+
    #        scale_fill_lancet()+
   #         theme_classic()
  #p1 + p2
p1
}
