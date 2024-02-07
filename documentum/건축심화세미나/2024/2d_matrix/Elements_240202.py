import numpy as np
np.set_printoptions(precision=4, suppress=True)

# V1.000

class Elements2D:
    elements_list = []
    def __init__(self, node1, node2):
        self.nodes = [node1, node2]
        self.node1 = node1
        self.node2 = node2
        self.x1 = node1.x
        self.x2 = node2.x
        self.y1 = node1.y
        self.y2 = node2.y
        self.length = ( (self.x2 - self.x1)**2 + (self.y2 - self.y1)**2 )**0.5
        self.element_force = [] #해석 결과 저장위치
        Elements2D.elements_list.append(self)# element list 정의



    def Truss2D(self, A, E): # 동일하게 3x3 매트릭스가 되도록 행렬 수정하기 
        rx = (self.x2 - self.x1) / self.length #λx
        ry = (self.y2 - self.y1) / self.length #λy
        print("λx , λy", rx, ry)

        self.k = A * E / self.length * np.array([
            [rx**2, rx*ry, -rx**2,-rx*ry],
            [rx*ry , ry**2, -rx*ry, -ry**2],
            [-rx**2, -rx*ry, rx**2,rx*ry],
            [-rx*ry , -ry**2, rx*ry, ry**2]
            ])
        # T' k' T 메트릭스를 미리 풀어서 입력했음. (물론 예제가 미리 풀어줬음)

    def Frame2D(self,A,I,E):
        rx = (self.x2 - self.x1) / self.length #λx
        ry = (self.y2 - self.y1) / self.length #λy
        print("λx , λy", rx, ry)
        L = self.length 

        T = np.array([
            [rx,ry,0,0,0,0],
            [-ry,rx,0,0,0,0],
            [0,0,1,0,0,0],
            [0,0,0,rx,ry,0],
            [0,0,0,-ry,rx,0],
            [0,0,0,0,0,1]
            ])
        T_t = np.array([
            [rx,-ry,0,0,0,0],
            [ry,rx,0,0,0,0],
            [0,0,1,0,0,0],
            [0,0,0,rx,-ry,0],
            [0,0,0,ry,rx,0],
            [0,0,0,0,0,1]
            ]) #transvers of T matrix

        k_lc = np.array([
            [A*E/L,0,0,-A*E/L,0,0],
            [0,12*E*I/L**3,6*E*I/L**2,0,-12*E*I/L**3,6*E*I/L**2],
            [0,6*E*I/L**2,4*E*I/L,0,-6*E*I/L**2,2*E*I/L],
            [-A*E/L,0,0,A*E/L,0,0],
            [0,-12*E*I/L**3,-6*E*I/L**2,0,12*E*I/L**3,-6*E*I/L**2],
            [0,6*E*I/L**2,2*E*I/L,0,-6*E*I/L**2,4*E*I/L]
            ])

        self.k = T_t @ k_lc @ T
        self.k_lc = k_lc
        self.T = T


        pass

    def PinFix(self,node1, node2):
        pass

    @classmethod
    def get_elements_list(cls):
        return cls.elements_list


class Nodes:
    nodes_list = []
    boundary_DOF = [] # 반력을 산출해야 하는 자유도 번호 정리
    def __init__(self, x, y):
        self.x = x
        self.y = y
        Nodes.nodes_list.append(self)# node list 정의
        number_of_nodes = len(Nodes.nodes_list)
        self.DOF= [number_of_nodes*3-2,number_of_nodes*3-1,number_of_nodes*3] # Node 별 자유도 자동배치
    
    def DefineDOF(self,degree_of_freedom):
        self.DOF = degree_of_freedom
        pass #노드별 자유도값 가지게 하기

    def mass(self):
        pass

    def fix(self,x,y,Mz=0):
        
        if x == 1: 
            Nodes.boundary_DOF.append(self.DOF[0])
        if y == 1: 
            Nodes.boundary_DOF.append(self.DOF[1])
        if Mz == 1:
            Nodes.boundary_DOF.append(self.DOF[2])



    @classmethod 
    def get_nodes_list(cls):
        return cls.nodes_list




class ElasticSolver:
    def __init__(self): 
        # 아래 리스트의 값은 각자 클래스명으로 활용 가능. ex) nodes_list_from_class[1].x
        self.nodes_list_from_class = Nodes.get_nodes_list()
        self.elements_list_from_class = Elements2D.get_elements_list()
        self.DOF_all = [];
        for i in range(0, len(self.nodes_list_from_class)):
            self.DOF_all = self.DOF_all + self.nodes_list_from_class[i].DOF
        self.DOF_all.sort()
        print("all dof : ",self.DOF_all)

        pass

    def Build_Matrix(self, DOF_per_node): # DOF per node 입력 없이, truss matrix 수정후 수정
        nodes = list(self.nodes_list_from_class)
        elements = list(self.elements_list_from_class)

        total_DOF = len(nodes) * DOF_per_node # 이부분은 해석 모델 특성에 따라 변하도록 확장 할것 
        global_matrix = np.zeros([total_DOF,total_DOF])
    
        for i_el in range(0,len(elements)):
            local_k = elements[i_el].k   
            local_index = np.array(elements[i_el].node1.DOF + elements[i_el].node2.DOF)-1
            # element 별로 가진 index 정리. -1 을 한 이유는 자유도 시작번호 1 list index 시작번호 0 매치 위함
    
            print(local_index+1)
            for i in range(0,len(local_index)):
                for j in range(0,len(local_index)):
                    global_matrix[local_index[i]][local_index[j]]=global_matrix[local_index[i]][local_index[j]]+local_k[i][j];
        self.total_matrix = global_matrix
        print(global_matrix)
        return global_matrix


    def ReduceMatrix(self):
        BDOF = Nodes.boundary_DOF

        DOF_free = list(self.DOF_all)
        for i in range(0,len(BDOF)):
            DOF_free.remove(BDOF[i])

        print("Free DOF : ",DOF_free)
        



        #변위 산출 매트릭스
        k = np.zeros([len(DOF_free),len(DOF_free)])
        for i in range(0,len(DOF_free)):
            for j in range(0,len(DOF_free)):
                k[i][j] = self.total_matrix[DOF_free[i]-1][DOF_free[j]-1]
        self.free_stiffness = k
        print(k)

        #반력 산출 매트릭스
        k = np.zeros([len(BDOF),len(BDOF)])
        for i in range(0,len(BDOF)):
            for j in range(0,len(BDOF)):
                k[i][j] = self.total_matrix[BDOF[i]-1][BDOF[j]-1]
        self.fix_stiffness = k
        print(k)

        

    def SolveStructure(self):

        BDOF = list(Nodes.boundary_DOF)

        DOF_free = list(self.DOF_all)
        for i in range(0,len(BDOF)):
            DOF_free.remove(BDOF[i])
        
        force_free = np.zeros(len(DOF_free))
        for i in range(0,len(force_free)):
            force_free[i] = Load.p_matrix[DOF_free[i]-1]

        force_boundary = np.zeros(len(BDOF))
        for i in range(0,len(BDOF)):
            force_boundary[i] = Load.p_matrix[BDOF[i]-1]


        disp_free = force_free @ np.linalg.inv(self.free_stiffness) 
        print( disp_free ) 

        self.structure_displacement_free = disp_free # 자유 node의 displacement 만 저장
        
        disp = np.zeros(len(self.DOF_all))
        for i in range(0,len(disp_free)):
            disp[DOF_free[i]-1] = disp_free[i]

        self.structure_displacement_total = disp[:]

        print("disp",disp)
        force = Solve2.total_matrix @ disp
        print( "all force", force)

        

        # 빈 reactio에 force 메트릭스에서 boundary에 해당하는 값 + P matrix에서 boundary에 해당하는 값 더하기 
        reaction = np.zeros(len(BDOF))
        for i in range(0,len(BDOF)):
            reaction[i] = force[BDOF[i]-1] - force_boundary[i]#부호결과 검증 할것


        print("reaction", reaction)


    def FindMemberElement(self):

        e_list = self.elements_list_from_class
        for ie in range(len(e_list)):
            print("emelement No.", ie+1 )            
            #Element 양 쪽 node 추출
            # node 별 자유도 정렬 -> element를 정의 할때 node 순서로 // node 1 2 순서로 매트릭스 생성 -> 부를때도 똑같음.
            temp_element_DOF = self.nodes_list_from_class[self.nodes_list_from_class.index(e_list[ie].node1)].DOF + self.nodes_list_from_class[self.nodes_list_from_class.index(e_list[ie].node2)].DOF

            print(temp_element_DOF)


            # 자유도에 해당하는 변위값 추출, -> element_disp
            # 해당 element의 T matrix 불러오기 
            # q = 부재력  k_e = element.k   T = element.T-> Tmatrix 객체값으로 정의 할것  D=추출된 변위 값 
            D = np.zeros(len(temp_element_DOF))
            for i in range(len(temp_element_DOF)):
                D[i] = self.structure_displacement_total[temp_element_DOF[i]-1]
            k_e = e_list[ie].k_lc
            T = e_list[ie].T

            q = k_e @ (T @ D)
            e_list[ie].element_force = q 

            print("k_e",k_e)
            print("T",T)
            print("D",D)
            print("d",T @ D)
            print('q',e_list[ie].element_force)


        #secs
        pass


class DefineLoad:
    def __init__(self): 
        self.DOF_all = [];
        for i in range(0, len(Nodes.nodes_list)):
            self.DOF_all = self.DOF_all + Nodes.nodes_list[i].DOF
        self.DOF_all.sort()
        self.p_matrix = np.zeros( len(self.DOF_all))
        pass

    def JointLoad(self,node_name,x,y,Mz):
        
        DOF_of_node = eval(node_name+".DOF")
        #node 의 dof와 일치하는 P matrix의 위치에 하중 입력 
        if x != 0: 
            self.p_matrix[DOF_of_node[0]-1] = x # + 방식으로 수정
        if y != 0: 
            self.p_matrix[DOF_of_node[1]-1] = y
        if Mz != 0: 
            self.p_matrix[DOF_of_node[2]-1] = Mz

        print("P : ", self.p_matrix)
        pass




#########################running test###################################

# def doAnalysisOnOneFrame(nodelist, ):
#     for idx,v in enumerate(nodelist):
#         Elements2D(v,nodelist(idx+1))

#Set node coordination. 
print("ex 14.1")
n1 = Nodes(3,4)
n2 = Nodes(0,0)
n3 = Nodes(3,0)
#set element tag 
E1 = Elements2D(n2, n3)
E2 = Elements2D(n2, n1)
#define element properties 
E1.Truss2D(1,1)
E2.Truss2D(1,1)


# print(E1.nodes)
# print(E1.x1, E1.y1,   E1.x2, E1.y2)
print("length E1", E1.length)
print("length E2", E2.length)

print("k_E1= \n",E1.k)
print("k_E2= \n",E2.k)

#Node 선언시 자동으로 3개의 자유도를가지게 됨. 아래와 같이 수동으로 자유도 설정하여 예제 비교. 
n1.DefineDOF([5,6])
n2.DefineDOF([1,2])
n3.DefineDOF([3,4])




Solve = ElasticSolver()


print(Nodes.boundary_DOF) 
n1.fix(1,1,0) # x, y 방향 고정 Mz = 0 초기값
n3.fix(1,1,0)
print("boundary DOFs", Nodes.boundary_DOF)





grobal_K = Solve.Build_Matrix(2)
Solve.ReduceMatrix



############frame example#######################
Elements2D.elements_list=[] # 위에서 한 예제의 메모리 비우기
Nodes.nodes_list = []
Nodes.boundary_DOF = []
print("\nex 16.1")

n1 = Nodes(0,0)
n2 = Nodes(20*12,0)
n3 = Nodes(20*12,-20*12)

#set element tag 
E1 = Elements2D(n1, n2)
E2 = Elements2D(n2, n3)
#define element properties 


E1.Frame2D(10,500,29000)
E2.Frame2D(10,500,29000)
print("length E1", E1.length)
print("length E2", E2.length)

print("k_E1= \n",E1.k)
print("k_E2= \n",E2.k)




#예제와 비교를 위한 정의로, 알고리즘화 해야함. 아래 for문 안쪽에서 정의하면 될거같음. 
# x y Mz
n1.DefineDOF([4,6,5])
n2.DefineDOF([1,2,3])
n3.DefineDOF([7,8,9])

n1.fix(0,1,0)
n3.fix(1,1,1)


Load = DefineLoad()
Load.JointLoad("n2",5,0,0)
Load.JointLoad("n3",0,0,0)




Solve2 = ElasticSolver()

grobal_K = Solve2.Build_Matrix(3)


Solve2.ReduceMatrix()
Solve2.SolveStructure()
Solve2.FindMemberElement()



