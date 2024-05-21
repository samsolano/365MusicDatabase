typedef enum logic [6:0] {
           LUI      = 7'b0110111,
           AUIPC    = 7'b0010111,
           JAL      = 7'b1101111,
           JALR     = 7'b1100111,
           BRANCH   = 7'b1100011,
           LOAD     = 7'b0000011,
           STORE    = 7'b0100011,
           OP_IMM   = 7'b0010011,
           OP       = 7'b0110011,
           SYSTEM   = 7'b1110011
 } opcode_t;
        
typedef struct packed{
    logic [6:0] opcode;
    logic [4:0] rs1_addr;
    logic [4:0] rs2_addr;
    logic [4:0] rd_addr;
    logic rs1_used;
    logic rs2_used;
    logic rd_used;
    logic [3:0] alu_fun;
    logic memWrite;
    logic memRead2;
    logic memRead1;
    logic regWrite;
    logic [1:0] rf_wr_sel;
    //logic [2:0] mem_type;  //sign, size
    logic [31:0] pc;
    logic [31:0] mux_a_out;
    logic [31:0] mux_b_out;
    //logic [31:0] regIn;
    logic [31:0] rs1;
    logic [31:0] rs2;
    //logic [4:0] rd;
    logic [31:0] aluResult;
    logic [31:0] IR;
    logic [31:0] DOUT2;
    logic [31:0] PC_PLUS_FOUR;
    logic [2:0] PC_SEL;
} instr_t;

module OTTER_MCU(input CLK,
                input INTR,
                input RESET,
                input [31:0] IOBUS_IN,
                output [31:0] IOBUS_OUT,
                output [31:0] IOBUS_ADDR,
                output logic IOBUS_WR 
);           
    //logic [6:0] opcode;
    logic [31:0] pc, pc_value, jalr_pc, branch_pc, jump_pc, int_pc,A,B,
        I_immed,S_immed,U_immed,aluBin,aluAin,aluResult,rfIn,csr_reg, mem_data, J_immed, B_immed;
    
    logic [31:0] IR;
    logic memRead1,memRead2;
    
    logic pcWrite,regWrite,memWrite, op1_sel,mem_op,IorD,pcWriteCond,memRead;
    logic [1:0]  rf_sel, wb_sel, mSize;
    logic [2:0] opB_sel;
    logic [3:0]alu_fun;
    logic [1:0] opA_sel;
        logic [2:0] PC_SEL;
    logic br_lt,br_eq,br_ltu;
    logic StallF, StallD, FlushD, FlushE, masterStall;
    logic [1:0] ForwardAE, ForwardBE;
    
    HazardUnit HU (.RS1D(de_inst.rs1_addr), .RS1E(de_ex_inst.rs1_addr), .RS2D(de_inst.rs2_addr), .RS2E(de_ex_inst.rs2_addr),
                    .RDE(de_ex_inst.rd_addr), .RDM(ex_mem_inst.rd_addr), .RDW(wb_mem_inst.rd_addr),
                    .PCSRCE(de_ex_inst.PC_SEL), .RegWriteM(ex_mem_inst.regWrite), .RegWriteW(wb_mem_inst.regWrite),
                     .FlushE(FlushE), .FlushD(FlushD), .ForwardAE(ForwardAE),
                    .ForwardBE(ForwardBE), .opcode(de_ex_inst.opcode), .masterStall(masterStall), .rs1_used(de_inst.rs1_used), .rs2_used(de_inst.rs2_used));
//==== Instruction Fetch ===========================================

     logic [31:0] if_de_pc, next_pc, PLUS_FOUR;
     logic reset;
     
     
     //assign pcWrite = 1'b1; 	//Hardwired high, assuming now hazards
     //assign memRead1 = 1'b1; 	//Fetch new instruction every cycle

     
    //changes mux select from this to output of decoder

    
    PC_REG PCREG1 (.PC_RST(RESET), .PC_WE(!masterStall), .CLK(CLK), .PC_DIN(pc_value), .PC_COUNT(next_pc));
    MUX MUX1 (.JALR(jalr_pc), .BRANCH(branch_pc), .JAL(jump_pc), .MTVEC(32'b0), .MEPC(32'b0), .PC_SEL(PC_SEL), .PC_DIN(pc_value), .ADD_FOUR(PLUS_FOUR));
    
    assign PLUS_FOUR = next_pc+4;


    always_ff @(posedge CLK) begin
        if(!masterStall) begin
             if_de_pc <= next_pc;
        end
       
       
       

    end
     
//==== Instruction Decode ===========================================
    logic [31:0] de_ex_opA;
    logic [31:0] de_ex_opB;
    logic [31:0] de_ex_rs2;


    instr_t de_ex_inst, de_inst;
    
    opcode_t OPCODE;
    //assign OPCODE_t = opcode_t'(IR[6:0]);
    

    logic [31:0] test;
    logic [31:0] opA_forwarded;
    logic [31:0] opB_forwarded;
        assign de_inst.rs1_addr=IR[19:15];
        assign de_inst.rs2_addr=IR[24:20];
        assign de_inst.rd_addr= IR[11:7];
        assign test = A;
        assign de_inst.opcode = IR[6:0];
        assign de_inst.pc = if_de_pc;
        assign de_inst.IR = IR;
        assign de_inst.PC_SEL = PC_SEL;
        assign de_inst.PC_PLUS_FOUR = PLUS_FOUR;



    CU_DECODER Decoder (.op_code(de_inst.IR[6:0]), .funct3(de_inst.IR[14:12]), .ir_30(de_inst.IR[30]), .int_taken(0), 
                        .br_eq(br_eq), .br_lt(br_lt), .br_ltu(br_ltu), .ALU_FUN(alu_fun), .srcA_SEL(opA_sel),
                        .srcB_SEL(opB_sel), .PC_SEL(PC_SEL), .RF_SEL(rf_sel), .PC_WE(pcWrite), .RF_WE(regWrite), 
                        .memWE2(memWrite),  .memRDEN2(memRead2), .memRDEN1(memRead1)
                        );
                        
    REG_FILE RegFile (.en(wb_mem_inst.regWrite), .adr1(de_inst.rs1_addr), .adr2(de_inst.rs2_addr), .w_adr(wb_mem_inst.rd_addr),
                     .w_data(rfIn), .CLK(CLK), .rs1(A), .rs2(B));
                     
   IMMED_GEN IG (.Instruction(IR[31:7]), .U_TYPE(U_immed), .I_TYPE(I_immed), .S_TYPE(S_immed), .J_TYPE(J_immed), .B_TYPE(B_immed));
   
   ALU_SRCA_MUX ALU_MUX_A(.rs1(A), .U_TYPE(U_immed), .notIN(0), .srcA_SEL(opA_sel), .ALU_srca(aluAin));
   
   ALU_SRCB_MUX ALU_MUX_B (.rs2(B), .I_TYPE(I_immed), .S_TYPE(S_immed), .PROGRAM_COUNT(if_de_pc), .csr_RD(csr_reg), .srcB_SEL(opB_sel),
                            .ALU_srcB(aluBin));
   
    
   ForwardMux FA (.MuxSelect(ForwardAE), .ALU_MUX_OUT(aluAin), .ALU_RESULT_M(ex_mem_inst.aluResult),
                    .RESULTW(rfIn), .MUX_OUT(opA_forwarded));
                    
   ForwardMux FB (.MuxSelect(ForwardBE), .ALU_MUX_OUT(aluBin), .ALU_RESULT_M(ex_mem_inst.aluResult),
                    .RESULTW(rfIn), .MUX_OUT(opB_forwarded));


        assign de_inst.alu_fun = alu_fun;
        assign de_inst.rf_wr_sel = rf_sel;
        //assign de_inst.regIn = rfIn;
        assign de_inst.regWrite = regWrite;
        assign de_inst.memWrite = memWrite;
        assign de_inst.memRead2 = memRead2;
        assign de_inst.memRead1 = memRead1;
//        assign de_inst.mux_a_out = aluAin;
//        assign de_inst.mux_b_out = aluBin;
        assign de_inst.mux_a_out = opA_forwarded;
        assign de_inst.mux_b_out = opB_forwarded;
        assign de_inst.rs1 = A;
        assign de_inst.rs2 = B;
        assign de_inst.pc = if_de_pc;
        assign de_inst.DOUT2 = 0;
        assign de_inst.aluResult = 0;
        
       assign de_inst.rs1_used=    de_inst.rs1 != 0
                                     && de_inst.opcode != 7'b0110111 //LUI
                                    && de_inst.opcode != 7'b0010111 //AIUPC
                                    && de_inst.opcode != 7'b1101111; //JAL
        
        
        assign de_inst.rs2_used = de_inst.rs2 != 0 && de_inst.opcode != 7'b0100011 //store 
                                    && de_inst.opcode != 7'b1100011 //branch 
                                    && de_inst.opcode == 7'b0010011 //OPIMMEDIATE 
                                    && de_inst.opcode != 7'b0110111 //LUI
                                    && de_inst.opcode != 7'b0010111 //AUIPC 
                                    && de_inst.opcode != 7'b1100111 //JALR 
                                    && de_inst.opcode != 7'b0000011 //LOAD 
                                    && de_inst.opcode != 7'b1110011 //SYStem
                                    && de_inst.opcode != 7'b1101111; //JAL
                                    
        assign de_inst.rd_used = de_inst.rd_addr != 0 
                                    && de_inst.opcode != 7'b0100011 //STORE 
                                    && de_inst.opcode != 7'b1100011 //BRANCH 
                                    && de_inst.opcode != 7'b1101111; //JAL
                                    


                                
    
   //stop pc for one cc         
	always_ff @(posedge CLK) begin
        de_ex_inst<=de_inst;

	end
//==== Execute ======================================================
    
     
     instr_t ex_mem_inst;

     
     
//     ForwardMux FA (.MuxSelect(ForwardAE), .ALU_MUX_OUT(de_ex_inst.mux_a_out), .ALU_RESULT_M(ex_mem_inst.aluResult),
//                    .RESULTW(rfIn), .MUX_OUT(opA_forwarded));
                    
//     ForwardMux FB (.MuxSelect(ForwardBE), .ALU_MUX_OUT(de_ex_inst.mux_b_out), .ALU_RESULT_M(ex_mem_inst.aluResult),
//                    .RESULTW(rfIn), .MUX_OUT(opB_forwarded));    
     
     // Creates a RISC-V ALU
    ALU ALU (.alu_fun(de_ex_inst.alu_fun), .srcA(de_ex_inst.mux_a_out), .srcB(de_ex_inst.mux_b_out), .alu_result(aluResult)); // the ALU
    
    BRANCH_ADDR_GEN BAG (.rs1(A), .I_type(I_immed), .B_type(B_immed), .J_type(J_immed), .PC(if_de_pc), .jal(jump_pc),
                         .jalr(jalr_pc), .branch(branch_pc));
                         
    BRANCH_COND_GEN BCG (.rs1(A), .rs2(B), .br_eq(br_eq), .br_lt(br_lt), .br_ltu(br_ltu));
     
     assign de_ex_inst.aluResult = aluResult;
     
     


	always_ff @(posedge CLK) begin
	   ex_mem_inst <= de_ex_inst;
		  

	end


//==== Memory ======================================================
     

// Assignments for memory or I/O operations based on decoded instruction properties
    assign IOBUS_ADDR = ex_mem_inst.aluResult; // The address for memory or I/O operations
    assign IOBUS_OUT = ex_mem_inst.rs2;     // Data to be written for STORE instructions
    //assign IOBUS_WR = ex_mem_inst.memWrite; // Control signal for write operations
    instr_t wb_mem_inst;
    
    Memory data_memory (
        .MEM_CLK(CLK),
        .MEM_ADDR1(next_pc[15:2]),
        .MEM_RDEN1(de_inst.memRead1),
        
        .MEM_RDEN2(ex_mem_inst.memRead2),
        .MEM_WE2(ex_mem_inst.memWrite),
        .MEM_ADDR2(ex_mem_inst.aluResult),
        .MEM_DIN2(ex_mem_inst.mux_b_out),
        .MEM_SIZE(ex_mem_inst.IR[13:12]),
        .MEM_SIGN(ex_mem_inst.IR[14]),
        .MEM_DOUT2(mem_data),  // Data read from memory
        .MEM_DOUT1(IR),
        .IO_IN(IOBUS_IN), .IO_WR(IOBUS_WR)
    );
    
    
    
    //assign rfIn = (ex_mem_inst.memRead2 ? mem_data : ex_mem_inst.regWrite);  // Choose data for RF based on memory read or ALU result
    
    
    always_ff @(posedge CLK) begin
        wb_mem_inst <= ex_mem_inst;
        
    end
 
     
//==== Write Back ==================================================
     
   //assign wb_mem_inst.rd = ex_mem_inst.IR[11:7];
    assign wb_mem_inst.DOUT2 = mem_data;
    
    RF_MUX RF_MUX (.PC_PLUS_FOUR(wb_mem_inst.PC_PLUS_FOUR), .csr_RD(csr_reg), .DOUT2(wb_mem_inst.DOUT2), .ALU_RESULT(wb_mem_inst.aluResult),
                    .RF_SEL(wb_mem_inst.rf_wr_sel), .w_data(rfIn));
       
            
endmodule