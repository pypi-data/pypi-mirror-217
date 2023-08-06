# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@name: BaselineComparisonLineView.py

@author: Patrizio Bellan
@organization: Free University of Bozen-Bolzano, Faculty of Computer Science, Piazza Domenicani 3, 39100 Bolzano, Italy - Fondazione Bruno Kessler, Process and Data Intelligence, Via Sommarive 18, 38123 Trento, Italy
@email: patrizio.bellan@gmail.com

This file contains the interface for the comparison between the goldstandard annotation and Baseline 1 predictions

"""
import os
import sys
import requests
import tkinter as tk
import tkinter.font as tkFont
from copy import deepcopy
from pathlib import Path
from random import randint
from tkinter import filedialog

from PETAnnotationDataset.AnnotationDataset import AnnotationDataset
from PIL import Image

# from annotationdataset import AnnotationDataset
from Visualizers.Colors import Annotator_Colors, MARK_COLORS,GetAgreementColor, Agreement_Scale_Full_5


class ToolTipGateways:
    def __init__(self, widget):
        def on_enter(event):
            self.tooltip = tk.Toplevel()
            self.tooltip.overrideredirect(True)
            # self.tooltip.geometry(f'+{event.x_root + 15}+{event.y_root + 10}')

            self.labelXOR = tk.Label(self.tooltip, text='XOR Gateway', bg=MARK_COLORS['XOR Gateway'])
            self.labelAND = tk.Label(self.tooltip, text='AND Gateway', bg=MARK_COLORS['AND Gateway'])
            self.labelXOR.pack()
            self.labelAND.pack()

        def on_leave(event):
            # if time() - self.show_start < 0.5:
            #     sleep(0.5)
            self.tooltip.destroy()

        self.widget = widget

        self.widget.bind('<Enter>', on_enter)
        self.widget.bind('<Leave>', on_leave)


# =============================================================================
# # FrameDocumentChunk
# =============================================================================
class TokenLineView(tk.Frame):
    def __init__(self, parent, dataset=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry('950x600')
        self.parent.title('Token Line View')
        if not dataset:
            while True:
                dataset_filename = Path(filedialog.askopenfilename())
                if dataset_filename:
                    dataset = AnnotationDataset()
                    if dataset.LoadDataset(dataset_filename):
                        break
        self.dataset = dataset

        # init variables
        self.__init__varialbles__()
        self.CreateFonts()
        # create interface
        self.createGUI()
        self.LoadDocumentsList()
        # update frame
        self.DocumentsListChanged()

    def DocumentsListChanged(self, *events):
        # doc_names = list(self.dataset.dataset['documents'].keys())
        # # selected_docs =  list(self.lst_documents.curselection())
        self.document_list = [self.lst_documents.get(x) for x in
                              self.lst_documents.curselection()]  # [doc_names[index] for index in selected_docs]
        self.UpdateAnnotatorList()
        self.UpdateFrame()

    def UpdateAnnotatorList(self):
        # to know the common annotators among documents, I get the list of the annotator_name for each document.
        # then, the annotator_name present in the list as many time as the number of the documents are the common annotators
        # To get the annotators' list I look into the first sentence

        annotators = list()
        for doc_name in self.document_list:
            annotators.extend(
                    list([name for name in self.dataset.dataset['documents'][doc_name]['predictors'].keys()
                          if 'entities' in self.dataset.dataset['documents'][doc_name]['predictors'][name]])
            )
            # get annotators
            # pass
        # print(annotators)
        # print([annotators.count(annotator_name) for annotator_name in set(annotators)])
        annotators = [annotator
                      for annotator in set(annotators)
                      if annotator != '' and annotators.count(annotator) == len(self.document_list)]
        annotators.append(AnnotationDataset.gold_standard_annotator_name)

        self.lst_annotators.delete(0, 'end')
        for annotator in annotators:
            if annotator == 'Baseline 3':
                continue
            self.lst_annotators.insert(tk.END, annotator)
        self.annotator_list = annotators
        # #select all elements in annotators list
        self.lst_annotators.select_set(0, 'end')
        self.AnnotatorListChanged()

    def AnnotatorListChanged(self, *events):
        # print('AnnotatorChanged')
        self.annotator_list = list()
        for index in self.lst_annotators.curselection():
            self.annotator_list.append(self.lst_annotators.get(index))

        self.GenerateAnnotatorsColors()
        self.GenerateAnnotationLetters()

        self.UpdateFrame()

    def LoadDocumentsList(self):
        self.lst_documents.delete(0, 'end')
        for doc in sorted(self.dataset.GetGoldStandardDocuments()):
            self.lst_documents.insert(tk.END, doc)
        # select all elements in annotators list
        # self.lst_documents.select_set(0, 'end')

    def __init__varialbles__(self):
        self.doc_name_selection = 0  # used to scroll listbox
        self.annotator_list = list()
        self.RELAXED_ANNOTATIONS = tk.BooleanVar()

        self.DRAWS_ACTIVITY_CHK = tk.BooleanVar()
        self.DRAWS_ACTIVITY_CHK.set(True)
        self.DRAWS_GATEWAY_CHK = tk.BooleanVar()
        self.DRAWS_GATEWAY_CHK.set(True)
        self.DRAWS_CONDITION_SPECIFICATION_CHK = tk.BooleanVar()
        self.DRAWS_CONDITION_SPECIFICATION_CHK.set(True)
        self.DRAWS_ACTIVITYDATA_CHK = tk.BooleanVar()
        self.DRAWS_ACTIVITYDATA_CHK.set(True)
        self.DRAWS_FURTHER_SPECIFICATION_CHK = tk.BooleanVar()
        self.DRAWS_FURTHER_SPECIFICATION_CHK.set(True)
        self.DRAWS_ACTOR_CHK = tk.BooleanVar()
        self.DRAWS_ACTOR_CHK.set(True)

        self.COLOR_AGREEMENT = tk.BooleanVar()
        self.COLOR_AGREEMENT.set(True)

        self.AnnotationLetterIndex = 3
        self.width_closed = 20
        self.width_expanded = 130

        self.btnOpenCloseText = tk.StringVar()
        self.btnOpenCloseStatus = tk.BooleanVar()

        self.canvas_objects = []
        self.sentence_offset = 50

        # =============================================================================
        #         # FONTS
        # =============================================================================

        self.sentence__font_size = tk.IntVar()
        self.sentence_text_font_size = tk.IntVar()

        self.sentence__font_size.set(12)
        self.sentence_text_font_size.set(self.sentence__font_size.get())

        self.sentence_font_family = "Helvetica"
        self.sentence_text_font_family = "Helvetica"

        self.standard_font_color = 'black'
        # sentence number font
        # self.CreateFonts()
        # =============================================================================
        #         # Canvas Dimensions
        # =============================================================================
        self.canvas_height = 50
        self.canvas_width = 50

        # =============================================================================
        #         # X, Y starting points
        # =============================================================================
        self.x_initial = 100  # x sep sentence number | sentence
        self.y_initial = 10  # initial y to start from

        self.x_sentence_number_start = 10

        # =============================================================================
        #         # Draw Objects
        # =============================================================================
        # Dashed H line
        self.dashed_width = 1

        self.annotation_width = tk.IntVar()
        self.annotation_width.set(5)

        # extra space around dashed line
        self.y_pad = 5
        # extra space before sentence text
        self.x_pad = 5

        self.vline = None

        self.annotator_colors = {'doc_name': 'deep sky blue'}
        # =============================================================================
        #         # Annotator's color
        # =============================================================================

    def GenerateAnnotatorsColors(self):
        """
            Generate random colors for the annotator_name marks
        """
        self.annotator_colors = {'doc_name': 'deep sky blue'}

        self.annotator_colors.update(
                {annotator_name: Annotator_Colors[randint(0, len(Annotator_Colors) - 1)]
                 for annotator_name in self.annotator_list})

    # =============================================================================
    #         # Annotator Letter
    # =============================================================================   
    def GenerateAnnotationLetters(self):
        self.annotatorLetter = {annotator_name: annotator_name[:self.AnnotationLetterIndex]
                                for annotator_name in self.annotator_list}

    def DeleteAll(self):
        self.canvas.delete('all')

    def DrawDocumentName(self, y_start, doc_name):
        """
            Draw document name
        """

        # Y
        y_start = y_start + self.sentence_text_font.cget('size')

        # X
        annotator_letter_size = tkFont.Font(font=self.sentence_text_font).measure(doc_name + '   ')

        x_start = self.x_initial - annotator_letter_size

        id_on_canvas_ = self.canvas.create_text(
                x_start,
                y_start,
                text=doc_name,  # self.annotatorLetter[annotator_name],
                font=self.sentence_text_font,
                fill=self.annotator_colors['doc_name'],
                anchor='nw')

        return id_on_canvas_, y_start

    def UpdateFrame(self, *events):
        self.DeleteAll()
        self.canvas_objects = []
        self.canvas_height = 50
        self.canvas_width = 50
        self.CreateFonts()
        self.DrawVerticalLine()
        self.PopulateCanvas()

    def CreateFonts(self):
        self.sentence_text_font = tkFont.Font(
                family=self.sentence_font_family,
                size=self.sentence__font_size.get())

        self.annotator_mark_font = tkFont.Font(
                family=self.sentence_text_font_family,
                size=self.annotation_width.get())

    def select_all_docs(self):
        self.lst_documents.selection_set(0, 'end')
        self.DocumentsListChanged()

    def createGUI(self):
        # frame
        self.Frame = tk.Frame(self.parent)
        # =============================================================================
        #         COMMANDS
        # =============================================================================
        self.frmCommands = tk.Frame(self.Frame)
        self.frmCommands.pack(fill='x')
        self.frmCommands.pack_propagate(0)

        # frm_top = tk.Frame(self.frmCommands)
        # frm_top.pack(
        #             # side='left',
        #              fill='x')

        # self.btnOpenClose = tk.Button(self.frmCommands,
        #                               textvariable=self.btnOpenCloseText,
        #                               command=self.OpenClose)
        # self.btnOpenClose.pack(side='left',
        #                        fill='x')

        frmlbl_docs = tk.LabelFrame(self.frmCommands, text='Documents')
        frmlbl_docs.pack(side='left', fill='both', expand=True)
        self.lst_documents = tk.Listbox(frmlbl_docs,
                                        selectmode='multiple',
                                        exportselection=False,
                                        height=7,
                                        width=35
                                        )
        # height = 4)
        self.lst_documents.pack(side='left', expand=True, fill='both')
        scrollbar_doc = tk.Scrollbar(frmlbl_docs)
        scrollbar_doc.pack(side=tk.RIGHT, fill='y')
        self.lst_documents.config(yscrollcommand=scrollbar_doc.set)
        scrollbar_doc.config(command=self.lst_documents.yview)
        self.lst_documents.bind('<<ListboxSelect>>', self.DocumentsListChanged)

        self.lst_documents.bind("<Down>", self.LstDocOnEntryDown)
        self.lst_documents.bind("<Up>", self.LstDocOnEntryUp)

        # LIST ANNOTATORS
        secondframe = tk.Frame(self.frmCommands)
        secondframe.pack(fill='both', side='left', expand=True)
        tk.Button(secondframe, text='select all docs', command=self.select_all_docs).pack(side='top', fill='x')
        frmlbl_anns = tk.LabelFrame(secondframe, text='Annotators')
        frmlbl_anns.pack(
                side='top',
                fill='x',
                expand=True
        )
        self.lst_annotators = tk.Listbox(frmlbl_anns,
                                         selectmode='multiple',
                                         exportselection=False,
                                         height=4,
                                         )
        self.lst_annotators.pack(side='left')
        scrollbar_ann = tk.Scrollbar(frmlbl_anns)
        scrollbar_ann.pack(side=tk.RIGHT, fill='y')
        self.lst_annotators.config(yscrollcommand=scrollbar_ann.set)
        scrollbar_ann.config(command=self.lst_annotators.yview)
        self.lst_annotators.bind('<<ListboxSelect>>', self.AnnotatorListChanged)

        frmlbl_ls = tk.LabelFrame(self.frmCommands,
                                  # self.frmCommands,
                                  text='Line Settings')
        frmlbl_ls.pack(side='left', fill='x', expand=True)

        self.sclMarkingThick = tk.Scale(frmlbl_ls,
                                        label='Line Size',
                                        length=100,
                                        variable=self.annotation_width,
                                        orient='horizontal',
                                        from_=1,
                                        to=13,
                                        command=self.UpdateFrame)
        self.sclMarkingThick.pack(side='left')

        self.sclTextFont = tk.Scale(frmlbl_ls,
                                    label='Text Size',
                                    length=100,
                                    variable=self.sentence__font_size,
                                    orient='horizontal',
                                    from_=7,
                                    to=32,
                                    command=self.UpdateFrame
                                    )
        self.sclTextFont.pack(side='left')
        self.COLOR_AGREEMENT.set(False)
        self.RELAXED_ANNOTATIONS.set(False)
        ############ PROCESS ELEMENTS ######################
        frmlbl_pe_re = tk.LabelFrame(self.frmCommands, text='Process Elements to Show')
        frmlbl_pe_re.pack(
                side='left',
                fill='both',
                expand=True
        )
        frmlbl_pe = tk.Frame(frmlbl_pe_re)
        frmlbl_pe.pack(side='left', fill='y')

        # ACTIVITY
        tk.Checkbutton(frmlbl_pe,
                       text='Show Activity',
                       variable=self.DRAWS_ACTIVITY_CHK,
                       command=self.UpdateFrame,
                       background=MARK_COLORS['Activity'],
                       # justify=tk.LEFT
                       ).pack(side='top',
                              fill='x')

        # FURTHER SPECIFICATION
        tk.Checkbutton(frmlbl_pe,
                       text='Show Further Specification',
                       variable=self.DRAWS_FURTHER_SPECIFICATION_CHK,
                       command=self.UpdateFrame,
                       background=MARK_COLORS['Further Specification'],
                       ).pack(
                side='top',
                anchor='w',
                fill='x')

        tk.Checkbutton(frmlbl_pe,
                       text='Show Activity Data',
                       variable=self.DRAWS_ACTIVITYDATA_CHK,
                       command=self.UpdateFrame,
                       background=MARK_COLORS['Activity Data'],
                       ).pack(side='top',
                              anchor='w',
                              fill='x')
        frmlbl_pe2 = tk.Frame(frmlbl_pe_re)
        frmlbl_pe2.pack(side='left', fill='y')

        tk.Checkbutton(frmlbl_pe2,
                       text='Show Actor',
                       variable=self.DRAWS_ACTOR_CHK,
                       command=self.UpdateFrame,
                       background=MARK_COLORS['Actor'],
                       ).pack(side='top',
                              anchor='w',
                              fill='x')
        chkShowGateway = tk.Checkbutton(frmlbl_pe2,
                                        text='Show Gateway',
                                        variable=self.DRAWS_GATEWAY_CHK,
                                        command=self.UpdateFrame,
                                        background=MARK_COLORS['XOR Gateway'],
                                        # justify=tk.LEFT
                                        )
        chkShowGateway.pack(side='top',
                            anchor='w',
                            fill='x')
        ToolTipGateways(chkShowGateway)

        tk.Checkbutton(frmlbl_pe2,
                       text='Show Condition Specification',
                       variable=self.DRAWS_CONDITION_SPECIFICATION_CHK,
                       command=self.UpdateFrame,
                       background=MARK_COLORS['Condition Specification'],
                       ).pack(side='top',
                              anchor='w',
                              fill='x')

        ############ PROCESS ELEMENTS ######################

        # =============================================================================
        # =============================================================================

        self.Expand()

        self.canvas = tk.Canvas(self.Frame,
                                bg="white",
                                height=self.canvas_height,
                                width=self.canvas_width,
                                # scrollregion=(0,0,self.canvas_height,self.canvas_width)
                                )

        self.hbar = tk.Scrollbar(self.Frame, orient='horizontal')
        self.hbar.pack(side='top', fill='x')
        self.hbar.config(command=self.canvas.xview)

        self.vbar = tk.Scrollbar(self.Frame, orient='vertical')
        self.vbar.pack(side='left', fill='y')
        self.vbar.config(command=self.canvas.yview)

        # self.canvas.config(width=300,height=300)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.config(
                scrollregion=(self.canvas.bbox("all"))
        )
        # self.canvas.scrollregion=(0,0,3500,3500)

        self.canvas.pack(fill='both', expand=True)

        self.Frame.pack(fill='both', expand=True)

        # vline
        self.DrawVerticalLine()

        # self.PopulateCanvas()
        # self.TestDrawing()

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def ShowAgreementScale(self):
        agreement_scale = tk.Toplevel(self.parent)

        for agree in range(100, -1, -20):
            color = GetAgreementColor(agree / 100, Agreement_Scale_Full_5)

            lbl_ = tk.Label(agreement_scale,
                            text='Agreement: {}%'.format(agree),
                            bg=color
                            )
            lbl_.pack(side='top',
                      fill='x')

    def OpenClose(self):
        if self.btnOpenCloseStatus.get():
            self.Close()
        else:
            self.Expand()

    def Close(self):
        self.frmCommands.config(height=self.width_closed)
        # self.Frame.config(height=self.parent.winfo_height())
        self.btnOpenCloseText.set('Open Commands')
        self.btnOpenCloseStatus.set(False)
        # print('navi closed')

    def Expand(self):
        self.frmCommands.config(height=self.width_expanded)
        # self.Frame.config(height=self.parent.winfo_height())
        self.btnOpenCloseText.set('Close Commands')
        self.btnOpenCloseStatus.set(True)
        # print('navi opened')

    def SaveCanvas(self):
        filename = Path(filedialog.asksaveasfilename())

        if filename:
            filename = str(filename.absolute())
            self.canvas.postscript(file=filename + '.eps')
            # use PIL to convert to PNG
            img = Image.open(filename + '.eps')
            img.save(filename + '.png', 'png')

    def CheckCanvasSize(self, current_y, current_x):
        changed = False
        # print(current_y > self.canvas_height, current_x > self.canvas_width)

        if current_y > self.canvas_height:
            self.canvas_height = current_y
            changed = True
        if current_x > self.canvas_width:
            self.canvas_width = current_x
            changed = True
        if changed:
            # print('changing dimensions')
            # print('previous', self.canvas.bbox("all"))
            self.canvas.config(width=self.canvas_width)
            self.canvas.config(height=self.canvas_height)

            self.canvas.config(
                    scrollregion=(self.canvas.bbox("all"))
            )

            self.hbar.config(command=self.canvas.xview)
            self.vbar.config(command=self.canvas.yview)
            self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

            self.DrawVerticalLine()
            # print('changed', self.canvas.bbox("all"))

    # =============================================================================
    #     # Drawing     
    # =============================================================================

    # =============================================================================
    #         # vline 
    # =============================================================================
    def DrawVerticalLine(self):
        self.vline = self.canvas.create_line(self.x_initial, 0, self.x_initial, self.canvas_height, fill='black',
                                             width=1)

    # =============================================================================
    #         # h dashed line 
    # =============================================================================
    def DrawHorizontalDashedLine(self, y_pos):
        y_pos = y_pos + self.sentence_text_font.cget('size') + self.y_pad
        self.vline = self.canvas.create_line(0, y_pos, self.canvas_width, y_pos, fill='black', width=self.dashed_width,
                                             dash=(2, 5))

        return y_pos + self.dashed_width + self.y_pad

    # =============================================================================
    #         # v dashedn temp dev line 
    # =============================================================================
    def DrawVDashLine(self, x_start, color):
        self.vline = self.canvas.create_line(x_start, 0, x_start, self.canvas_height, fill=color, width=1, dash=(1, 2))

    def DrawVDashLine2(self, x_start, y_pos, y_end, color):
        self.vline = self.canvas.create_line(x_start, y_pos, x_start, y_end, fill=color, width=1, dash=(1, 2))

    # =============================================================================
    #         # annotation h line 
    # =============================================================================

    #     # THIS IS THE OLD METHOD
    # def DrawHAnnotationdLine(self, y_pos, 
    #                          x_start,
    #                          x_end, 
    #                          annotator_name, 
    #                          is_other=False):

    #     y_pos = y_pos + self.sentence_text_font.cget('size') - self.annotation_width.get()

    #     if is_other:
    #         id_annotation_lines = self.canvas.create_line(x_start, 
    #                                          y_pos, 
    #                                          x_end,
    #                                          y_pos, 
    #                                          fill = self.annotator_colors[annotator_name], 
    #                                          width = self.annotation_width.get(),
    #                                              dash=(2,3)
    #                                          )

    #     else: 
    #         # is an activity
    #         id_annotation_lines = self.canvas.create_line(x_start, 
    #                                              y_pos, 
    #                                              x_end,
    #                                              y_pos, 
    #                                              fill = self.annotator_colors[annotator_name], 
    #                                              width = self.annotation_width.get()
    #                                              )

    #     return id_annotation_lines

    def DrawHAnnotationdLine(self,
                             y_pos,
                             x_start,
                             x_end,
                             color):

        # y_pos = y_pos + self.sentence_text_font.cget('size') - self.annotation_width.get()
        # y_pos = y_pos  - self.annotation_width.get()
        id_annotation_lines = self.canvas.create_line(
                x_start,
                y_pos,
                x_end,
                y_pos,
                fill=color,
                width=self.annotation_width.get()
        )

        return id_annotation_lines

    # =============================================================================
    def DrawAnnotatorLetter(self,
                            y_start,
                            annotator_name):
        """
            Draw annotation letter or (abbreviation) of an annotator_name
        """

        # Y

        y_start = y_start + self.sentence_text_font.cget('size')

        # X
        annotator_letter_size = tkFont.Font(font=self.sentence_text_font).measure(
                self.annotatorLetter[annotator_name] + '   ')

        x_start = self.x_initial - annotator_letter_size

        id_on_canvas_ = self.canvas.create_text(
                x_start,
                y_start,
                text=self.annotatorLetter[annotator_name],
                font=self.sentence_text_font,
                fill=self.annotator_colors[annotator_name],
                anchor='nw')

        return id_on_canvas_, y_start

    # =============================================================================
    def DrawAnnotatorLetters(self, y_start):
        """
            Draws annotators letters (or abbreviations)
            
            input:
                y_start: int
                    y coordinate to start drawing texts
                
            output:
                y_end: int
                    final y position
                
                ids_annotator_letters,
                    [annotator_name] =  id text object in the canvas
                
                ys_pos: dict
                    [annotator_name] = y_position
        """
        ids_annotator_letters = {}
        ys_pos = {}
        for annotator_name in self.annotator_list:
            id_on_canvas, y_start = self.DrawAnnotatorLetter(y_start, annotator_name)

            ids_annotator_letters[annotator_name] = id_on_canvas
            ys_pos[annotator_name] = y_start

        y_end = y_start

        return y_end, ids_annotator_letters, ys_pos

    # =============================================================================
    def DrawSentenceNumber(self, y_start, sentence_number):
        """
            Draws sentence number    
  
            input:
                y_start: int
                    y coordinate to start drawing text
                    
            output:
                y_end: int
                    final y position   
                
                id_on_canvas: inr
                    id text object in the canvas
        """

        y_start = y_start + self.sentence_text_font.cget('size')
        # sentence_number_size = tkFont.Font(font=self.sentence_text_font).measure(sentence_number+' ')
        # x_start = self.x_initial - sentence_number_size 
        id_on_canvas = self.canvas.create_text(
                self.x_sentence_number_start,
                y_start,
                text=sentence_number,
                font=self.sentence_text_font,
                # fill=self.annotator_colors[annotator_name],
                anchor='nw')

        # add sentence offset 
        # y_end = y_sentence_number + self.sentence_offset
        y_end = y_start

        return y_end, id_on_canvas

        # =============================================================================

    def DrawSentence(self,
                     y_start,
                     sentence_number,
                     sentence_list,
                     annotations,
                     doc_name):

        # =============================================================================
        #  # left side of the vline
        # =============================================================================
        y_end, ids_annotator_letters, ys_pos_annotators = self.DrawAnnotatorLetters(y_start)
        y_end, id_sentence_on_canvas = self.DrawSentenceNumber(y_end,
                                                               sentence_number)
        ys_pos_annotators['sentence-text'] = y_end
        # =============================================================================
        #  # right side of the vline
        #         # Draw Sentence
        # =============================================================================
        id_sentenceText_on_canvas = self.DrawTextSentence(y_end,
                                                          sentence_list,
                                                          int(sentence_number),
                                                          doc_name)
        # =============================================================================
        # Mark The Sentence
        # =============================================================================
        ids_annotation_marks = self.MarkSentence(
                y_end,
                ys_pos_annotators,
                id_sentenceText_on_canvas,
                annotations,
                int(sentence_number))

        # if self.DRAWS_OTHER.get():
        #     ids_annotation_marks = self.MarkSentence(   
        #                                             y_end,
        #                                             ys_pos_annotators,
        #                                           id_sentenceText_on_canvas,
        #                                           annotations['Other'], 
        #                                           is_other=True)
        # =============================================================================
        #         # horizontal Sep Line
        # =============================================================================
        y_end = self.DrawHorizontalDashedLine(y_end)

        # check canvas dimenions
        self.CheckCanvasSize(y_end + self.y_pad * 2, self.canvas_width)

        return y_end  # , ys_pos_annotators, ids_annotation_marks

    # =============================================================================
    def DrawTextSentence(self, y_start,
                         sentence_list,
                         n_sent,
                         doc_name):
        #         def GetColor(process_element_tag, show_var=None):
        # ##### DEV QUESTO!!!!
        #             if process_element_type == 'Activity' and not self.DRAWS_ACTIVITY_CHK.get():
        #                 scores.pop('Activity')
        #
        #                 # invert dict
        #                 scores_inv = {v: k for k, v in scores.items()}
        #                 try:
        #                     max_val = max(scores_inv)
        #                     process_element_type = scores_inv[max_val]
        #                     # recompute max agreement
        #                     agreement = scores[process_element_type] / len_annotators
        #                     color = GetAgreementColor(agreement, Agreement_Scale_Full_5)
        #                 except ValueError:
        #                     # the dict is void, so not annotated
        #                     color = 'black'
        #
        #             return color

        len_annotators = len(self.annotator_list)

        words_ids_on_canvas = {}
        x_current = self.x_initial + self.x_pad
        for n_word, word in enumerate(sentence_list):
            # print (n_sent, n_word)
            # if n_sent == 1:
            # print()
            # if self.COLOR_AGREEMENT.get():
            #     # get agreement
            #     process_element_type, annotation_count, agreement, scores = self.dataset.GetWordAgreement(doc_name,
            #                                                                                               n_sent,
            #                                                                                               n_word,
            #                                                                                               self.annotator_list)
            #     try:
            #         scores.pop('')  # delete no annotation
            #         if len(scores) > 0:
            #
            #             scores_inv = {v: k for k, v in scores.items()}
            #
            #             max_val = max(scores_inv)
            #             process_element_type = scores_inv[max_val]
            #             # recompute max agreement
            #             agreement = scores[process_element_type] / len_annotators
            #             color = GetAgreementColor(agreement, Agreement_Scale_Full_5)
            #         else:
            #             color = 'black'
            #     except KeyError:
            #         # check that the max agreeded process element is also shown
            #         color = GetAgreementColor(agreement, Agreement_Scale_Full_5)
            #     if process_element_type == 'Activity' and not self.DRAWS_ACTIVITY_CHK.get():
            #         scores.pop('Activity')
            #
            #         # invert dict
            #         scores_inv = {v: k for k, v in scores.items()}
            #         try:
            #             max_val = max(scores_inv)
            #             process_element_type = scores_inv[max_val]
            #             # recompute max agreement
            #             agreement = scores[process_element_type] / len_annotators
            #             color = GetAgreementColor(agreement, Agreement_Scale_Full_5)
            #         except ValueError:
            #             # the dict is void, so not annotated
            #             color = 'black'
            #
            #     if process_element_type == 'Activity Data' and not self.DRAWS_ACTIVITYDATA_CHK.get():
            #         scores.pop('Activity Data')
            #         # invert dict
            #         scores_inv = {v: k for k, v in scores.items()}
            #         try:
            #             max_val = max(scores_inv)
            #             process_element_type = scores_inv[max_val]
            #             # recompute max agreement
            #             agreement = scores[process_element_type] / len_annotators
            #             color = GetAgreementColor(agreement, Agreement_Scale_Full_5)
            #         except ValueError:
            #             # the dict is void, so not annotated
            #             color = 'black'
            #
            #     if process_element_type == 'Actor' and not self.DRAWS_ACTOR_CHK.get():
            #         scores.pop('Actor')
            #         # invert dict
            #         scores_inv = {v: k for k, v in scores.items()}
            #         try:
            #             max_val = max(scores_inv)
            #             process_element_type = scores_inv[max_val]
            #             # recompute max agreement
            #             agreement = scores[process_element_type] / len_annotators
            #             color = GetAgreementColor(agreement, Agreement_Scale_Full_5)
            #         except ValueError:
            #             # the dict is void, so not annotated
            #             color = 'black'
            #     # set color of the max agreement
            # ####
            # # if process_element_type == '-' and len(scores)<=1:
            # #     color = 'black'
            # # else:
            # #     color = GetAgreementColor(agreement, Agreement_Scale_Full_5)
            # else:
            color = 'black'
            id_on_canvas = self.canvas.create_text(
                    # x
                    x_current,
                    # y
                    y_start,
                    text='{} '.format(word),
                    font=self.sentence_text_font,
                    anchor='nw',
                    fill=color,
            )
            _, _, x_end, _ = self.canvas.bbox(id_on_canvas)

            # x_end = 
            words_ids_on_canvas[n_word] = {'id': id_on_canvas, 'x_start': x_current, 'x_end': x_end}
            # draw a space between words
            x_current = x_end

        return words_ids_on_canvas

    # =============================================================================
    def DrawStartEndLines(self,
                          annotator_name,
                          annotation_label,
                          x_start,
                          x_end,
                          y_pos,
                          y_end):
        color = MARK_COLORS[annotation_label]

        y_pos = y_pos + self.annotation_width.get()
        id_ = self.DrawHAnnotationdLine(
                y_pos,
                x_start,
                x_end,
                color)
        # draw V dashed lines
        self.DrawVDashLine2(x_start, y_pos, y_end, color)  # self.annotator_colors[annotator_name])
        self.DrawVDashLine2(x_end, y_pos, y_end, color)  # self.annotator_colors[annotator_name])

        return id_

    def MarkSentence(self, y_end,
                     ys_pos_annotators,
                     words_ids_on_canvas,
                     annotations,
                     sentence_number):
        """
            Draws annotation marks over words
        """
        space_character = tkFont.Font(font=self.sentence_text_font).measure(' ')

        y_end = y_end + self.sentence_text_font.cget('size') + 1
        # self.DrawVDashLine(x_start_sent, 'black')
        # self.DrawVDashLine(x_end_sent,'black')
        for annotator_name in ys_pos_annotators:
            if annotator_name == 'sentence-text' or annotations[annotator_name] == []:
                continue
            y_pos = ys_pos_annotators[annotator_name]

            for annotation_label in annotations[annotator_name].keys():
                # if annotation_label == '-':
                #     continue
                if annotation_label == 'Activity' and not self.DRAWS_ACTIVITY_CHK.get():
                    continue
                if (
                        annotation_label == 'AND Gateway' or annotation_label == 'XOR Gateway') and not self.DRAWS_GATEWAY_CHK.get():
                    continue
                if annotation_label == 'Activity Data' and not self.DRAWS_ACTIVITYDATA_CHK.get():
                    continue
                if annotation_label == 'Actor' and not self.DRAWS_ACTOR_CHK.get():
                    continue
                if annotation_label == 'Condition Specification' and not self.DRAWS_CONDITION_SPECIFICATION_CHK.get():
                    continue
                if annotation_label == 'Further Specification' and not self.DRAWS_FURTHER_SPECIFICATION_CHK.get():
                    continue
                # =============================================================================
                #   New method
                for annotation_range in annotations[annotator_name][annotation_label][sentence_number]:
                    # annotation_range = annotations[annotator_name][annotation_label][sentence_number]
                    if not annotation_range:
                        continue
                    begin = words_ids_on_canvas[annotation_range[0]]['x_start']
                    end = words_ids_on_canvas[annotation_range[-1]]['x_end']
                    #
                    # for annotation_range in annotations[annotator_name][annotation_label][sentence_number]:
                    #     begin = words_ids_on_canvas[annotation_range[0]]['x_start']
                    #     end = words_ids_on_canvas[annotation_range[-1]]['x_end']
                    self.DrawStartEndLines(annotator_name,
                                           annotation_label,
                                           begin,
                                           end - space_character,  # remove the right hand space character,
                                           y_pos,
                                           y_end)

    def PopulateCanvas(self):
        # def TestDrawing(self):
        y_end = self.y_initial

        for n_doc, doc_name in enumerate(self.document_list):
            id_on_canvas_, y_end = self.DrawDocumentName(y_end, doc_name)
            # add space between doc name and ghe sentences
            y_end = y_end + 15

            annotations = {
                    AnnotationDataset.gold_standard_annotator_name: self.dataset.GetGoldStandardEntities(doc_name)}
            for annotator_name in self.annotator_list:
                if annotator_name == AnnotationDataset.gold_standard_annotator_name:
                    continue
                annotations[annotator_name] = \
                    self.dataset.dataset['documents'][doc_name]['predictors'][annotator_name]['entities']

            for n_sent in range(self.dataset.GetNSentences(doc_name)):
                sentence_list = self.dataset.GetSentenceListOfWords(doc_name, n_sent)
                try:
                    y_end = self.DrawSentence(
                            y_end,
                            str(n_sent),
                            sentence_list,
                            deepcopy(annotations),
                            doc_name)
                except:
                    print('er', doc_name, n_sent)
            # add space between doc name and the sentences
            y_end = y_end + 15

        self.canvas.focus_set()

    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            self.canvas.xview_scroll(scroll, "units")
        else:
            self.canvas.yview_scroll(scroll, "units")

    def LstDocOnEntryUp(self, event):
        if self.doc_name_selection < self.lst_documents.size():
            self.lst_documents.select_clear(self.doc_name_selection)
            self.doc_name_selection += 1
            self.lst_documents.select_set(self.doc_name_selection)
            self.DocumentsListChanged()

    def LstDocOnEntryDown(self, event):
        if self.doc_name_selection > 0:
            self.lst_documents.select_clear(self.doc_name_selection)
            self.doc_name_selection -= 1
            self.lst_documents.select_set(self.doc_name_selection)
            self.DocumentsListChanged()


def getdata():
    """
    this function downloads the dataset from github

    :return: 
    """
    url = "https://raw.githubusercontent.com/patriziobellan86/PETbaselines/master/petdatasetgoldstandardbaselines.json"
    resp = requests.get(url)
    with open("petdatasetgoldstandardbaselines.json", "w") as f:
        f.write(resp.text)

def Show():
    curdir = Path(os.path.curdir).absolute()
    curdir = curdir.joinpath('petdatasetgoldstandardbaselines.json')
    dataset_filename = curdir.absolute()
    dataset = AnnotationDataset()
    dataset.LoadDataset(filename=dataset_filename)

    window = tk.Tk()
    program = TokenLineView(window, dataset)
    # Start the GUI event loop
    program.mainloop()
    program.quit()
    sys.exit()


if __name__ == '__main__':
    getdata()
    Show()
