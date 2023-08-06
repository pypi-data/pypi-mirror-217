#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@name: BaselinePredictorAgreementInterface.py

@author: Patrizio Bellan
@organization: Free University of Bozen-Bolzano, Faculty of Computer Science, Piazza Domenicani 3, 39100 Bolzano, Italy - Fondazione Bruno Kessler, Process and Data Intelligence, Via Sommarive 18, 38123 Trento, Italy
@email: patrizio.bellan@gmail.com

This file contains the interface for the agreement between the baseline predictors

"""
import os.path
import tkinter as tk
import tkinter.ttk as ttk

import matplotlib.pyplot as plt
# from annotationdataset import AnnotationDataset
from PETAnnotationDataset.AnnotationDataset import AnnotationDataset
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Visualizers.CalculateBaselinePredictorsAgreement import CalculateBaselinePredictorsF1
from Visualizers.Colors import MARK_COLORS, PRECISION, RECALL, F1SCORE
from pathlib import Path
import requests


class ToolTipGateways:
    def __init__(self, widget):
        def on_enter(event):
            self.tooltip = tk.Toplevel()
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root + 15}+{event.y_root + 10}')

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


class ToolTipLegend:
    def __init__(self, widget):
        def on_enter(event):
            self.tooltip = tk.Toplevel()
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root + 15}+{event.y_root + 10}')

            self.labelprecision = tk.Label(self.tooltip, text='Precision', bg=PRECISION)
            self.labelrecall = tk.Label(self.tooltip, text='Recall', bg=RECALL)
            self.labelf1score = tk.Label(self.tooltip, text='F1 score', bg=F1SCORE)
            self.labelprecision.pack()
            self.labelrecall.pack()
            self.labelf1score.pack()

        def on_leave(event):
            # if time() - self.show_start < 0.5:
            #     sleep(0.5)
            self.tooltip.destroy()

        self.widget = widget

        self.widget.bind('<Enter>', on_enter)
        self.widget.bind('<Leave>', on_leave)


class F1BaselinePredictorsAgreement(tk.Frame):
    bar_size = 0.25
    precision_color = PRECISION
    recall_color = RECALL
    F1_color = F1SCORE

    pe_labels = ['Activity', 'Activity Data', 'Actor',
                 'XOR Gateway', 'AND Gateway', 'Condition Specification', 'Further Specification']
    re_labels = ['a4Flows',  # Sequence Flow',
                 'a2Uses',  # 'Uses',
                 'Actor Performer',  # 'Roles'
                 'Actor Recipient',  # 'Roles',
                 'a5FurtherSpecification',
                 'a6SameGateway',
                 # 'CorefActor',
                 # 'Coref' # act data
                 ]
    pe_labels_dict_plot = {k: k for k in pe_labels}

    re_labels_dict_plot = {'a4Flows':                'seq. flow',
                           'a2Uses':                 'uses',
                           'Actor Performer':        'actor.performer',
                           'Actor Recipient':        'actor.recipient',
                           'a5FurtherSpecification': 'further spec.',
                           'a6SameGateway':          'same gateway',
                           # 'CorefActor': 'coref.actor',
                           # 'Coref': 'coref.act data' # act data
                           }

    def __init__(self, parent, dataset):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry('1150x800')
        self.parent.title('Baseline Predictos Agreement')
        # self.parent.tk.call('wm', 'iconphoto', self.parent._w, tk.PhotoImage(file='agreementicon.png'))
        self.dataset = dataset
        plt.rcParams['toolbar'] = 'None'  # Disables matplotlib toolbar

        # init variables
        self.__init__varialbles__()

        # create interface
        self.CreateFrame()
        self.LoadDocumentsList()

    def __init__varialbles__(self):
        self.canvas_width = 2000
        self.canvas_height = 500

        self.F1 = tk.DoubleVar()

        self.annotator_list = list()
        # PE
        self.ACTIVITY_CHK = tk.BooleanVar()
        self.ACTIVITY_CHK.set(True)
        self.GATEWAY_CHK = tk.BooleanVar()
        self.GATEWAY_CHK.set(True)
        self.CONDITION_SPECIFICATION_CHK = tk.BooleanVar()
        self.CONDITION_SPECIFICATION_CHK.set(True)
        self.ACTIVITYDATA_CHK = tk.BooleanVar()
        self.ACTIVITYDATA_CHK.set(True)
        self.FURTHER_SPECIFICATION_CHK = tk.BooleanVar()
        self.FURTHER_SPECIFICATION_CHK.set(True)
        self.ACTOR_CHK = tk.BooleanVar()
        self.ACTOR_CHK.set(True)
        # RE
        self.RE_SEQUENCE_FLOW = tk.BooleanVar()
        self.RE_USES = tk.BooleanVar()
        # self.RE_ROLES = tk.BooleanVar()
        self.RE_ROLES_PERFORMER = tk.BooleanVar()
        self.RE_ROLES_RECIPIENT = tk.BooleanVar()
        self.RE_FURTHER_SPECIFICATION = tk.BooleanVar()
        self.RE_SAME_GATEWAY = tk.BooleanVar()
        self.RE_COREF_ACTIVITY_DATA = tk.BooleanVar()
        self.RE_COREF_ACTOR = tk.BooleanVar()

        self.RE_SEQUENCE_FLOW.set(True)
        self.RE_USES.set(True)
        # self.RE_ROLES.set(True)
        self.RE_ROLES_PERFORMER.set(True)
        self.RE_ROLES_RECIPIENT.set(True)
        self.RE_FURTHER_SPECIFICATION.set(True)
        self.RE_SAME_GATEWAY.set(True)
        self.RE_COREF_ACTIVITY_DATA.set(True)
        self.RE_COREF_ACTOR.set(True)

        self.ON_RELAXED_ANNOTATION = tk.BooleanVar()
        self.ON_RELAXED_ANNOTATION.set(True)

        # self.CALCULATE_ALL = tk.BooleanVar()
        # self.CALCULATE_ALL.set(True)
        self.axs = list()  # plot objects

        self.width_closed = 50
        self.width_expanded = 250
        self.btnOpenCloseText = tk.StringVar()
        self.btnOpenCloseStatus = tk.BooleanVar()

        # =============================================================================
        #         # Draw Objects
        # =============================================================================
        # Dashed H line
        self.dashed_width = 1

        # extra space around dashed line
        self.y_pad = 5
        # extra space before sentence text
        self.x_pad = 5

        # PLTs
        self.fig_pe_global = Figure(figsize=(13, 5), dpi=100)
        self.ax_pe_global = self.fig_pe_global.subplots(1, 1)  # add_subplot(111)
        self.fig_pe_doc = Figure(figsize=(13, 5), dpi=100)
        self.ax_pe_doc = self.fig_pe_doc.subplots(1, 1)  # add_subplot(111)
        self.fig_pe_pe = Figure(figsize=(13, 5), dpi=100)
        self.ax_pe_pe = self.fig_pe_pe.subplots(1, 1)  # add_subplot(111)

        self.fig_re_global = Figure(figsize=(13, 5), dpi=100)
        self.ax_re_global = self.fig_re_global.subplots(1, 1)  # add_subplot(111)
        self.fig_re_doc = Figure(figsize=(13, 5), dpi=100)
        self.ax_re_doc = self.fig_re_doc.subplots(1, 1)  # add_subplot(111)
        self.fig_re_re = Figure(figsize=(13, 5), dpi=100)
        self.ax_re_re = self.fig_re_re.subplots(1, 1)  # add_subplot(111)

    def DrawGraphsPe(self, agreement):
        self.DrawGraphsGlobal_pe(agreement)
        self.DrawGraphsDoc_pe(agreement)
        self.DrawGraphsPe_pe(agreement)

    def DrawGraphsRe(self, agreement):
        self.DrawGraphsGlobal_re(agreement)
        self.DrawGraphsDoc_re(agreement)
        self.DrawGraphsRe_re(agreement)

    def DrawGraphsPe_pe(self, agreement):
        supports = dict()
        self.ax_pe_pe.clear()
        for n_pe, pe in enumerate(self.pe_selected_labels):
            precision, recall, F1, supports[pe] = agreement.Compute_PR_REC_F1_process_element(pe)
            self.ax_pe_pe.bar(n_pe - .3, precision, color=self.precision_color, width=self.bar_size)
            self.ax_pe_pe.bar(n_pe, recall, color=self.recall_color, width=self.bar_size)
            self.ax_pe_pe.bar(n_pe + .3, F1, color=self.F1_color, width=self.bar_size)
        self.ax_pe_pe.set_xlim(-.5, n_pe + 0.5)
        self.ax_pe_pe.set_xticks([x for x in range(n_pe + 1)])
        self.ax_pe_pe.set_xticklabels(['{}\n{}'.format(self.pe_labels_dict_plot[lab], supports[lab])
                                       for lab in self.pe_selected_labels])
        # self.ax_pe_pe.set_title('Process Element\nAgreement')
        self.ax_pe_pe.spines['top'].set_visible(False)
        self.ax_pe_pe.spines['right'].set_visible(False)
        # new helper method to auto-label bars
        for container in self.ax_pe_pe.containers:
            self.ax_pe_pe.bar_label(container)
        self.fig_pe_pe.tight_layout()
        self.canvas_pe_pe_plot.draw()
        self.canvas_pe_pe.update()

    def DrawGraphsRe_re(self, agreement):
        self.ax_re_re.clear()
        supports = dict()
        for n_re, re in enumerate(self.re_selected_labels):
            precision, recall, F1, supports[re] = agreement.Compute_PR_REC_F1_relation_type(re)
            self.ax_re_re.bar(n_re - .3, precision, color=self.precision_color, width=self.bar_size)
            self.ax_re_re.bar(n_re, recall, color=self.recall_color, width=self.bar_size)
            self.ax_re_re.bar(n_re + .3, F1, color=self.F1_color, width=self.bar_size)
        self.ax_re_re.set_xlim(-.5, n_re + 0.5)
        self.ax_re_re.set_xticks([x for x in range(n_re + 1)])
        self.ax_re_re.set_xticklabels(['{}\n{}'.format(self.re_labels_dict_plot[lab], supports[lab])
                                       for lab in self.re_selected_labels])
        # self.ax_pe_pe.set_title('Process Element\nAgreement')
        self.ax_re_re.spines['top'].set_visible(False)
        self.ax_re_re.spines['right'].set_visible(False)
        # new helper method to auto-label bars
        for container in self.ax_re_re.containers:
            self.ax_re_re.bar_label(container)
        self.fig_re_re.tight_layout()
        self.canvas_re_re_plot.draw()
        self.canvas_re_re.update()

    def DrawGraphsDoc_re(self, agreement):
        supports = dict()
        self.ax_re_doc.clear()
        for n_doc, doc_name in enumerate(self.doc_list):
            precision, recall, F1, supports[doc_name] = agreement.Compute_PR_REC_F1_document_re(doc_name)
            # self.ax_re_doc.bar(n_doc-.5, precision, color=self.precision_color, width=self.bar_size)
            # self.ax_re_doc.bar(n_doc, recall, color=self.recall_color, width=self.bar_size)
            # self.ax_re_doc.bar(n_doc+.5, F1, color=self.F1_color, width=self.bar_size)
            # self.ax_re_doc.bar(n_doc - .5, precision, color=self.precision_color, width=self.bar_size)
            # self.ax_re_doc.bar(n_doc, recall, color=self.recall_color, width=self.bar_size)
            self.ax_re_doc.bar(n_doc, F1, color=self.F1_color, width=self.bar_size)
        self.ax_re_doc.set_xlim(-1, n_doc + 1)
        self.ax_re_doc.set_xticks([x for x in range(n_doc + 1)])
        self.ax_re_doc.set_xticklabels(['{}\n{}'.format(doc[:5],
                                                        agreement.support_re)
                                        for doc in self.doc_list])
        # self.ax_pe_doc.set_title('Document\nAgreement')
        self.ax_re_doc.spines['top'].set_visible(False)
        self.ax_re_doc.spines['right'].set_visible(False)
        # new helper method to auto-label bars
        for container in self.ax_re_doc.containers:
            self.ax_re_doc.bar_label(container)
        self.fig_re_doc.tight_layout()
        self.canvas_re_doc_plot.draw()
        self.canvas_re_doc.update()

    def DrawGraphsDoc_pe(self, agreement):
        supports = dict()
        self.ax_pe_doc.clear()
        for n_doc, doc_name in enumerate(self.doc_list):
            precision, recall, F1, supports[doc_name] = agreement.Compute_PR_REC_F1_document_pe(doc_name)
            # self.ax_pe_doc.bar(n_doc-.5, precision, color=self.precision_color, width=self.bar_size)
            # self.ax_pe_doc.bar(n_doc, recall, color=self.recall_color, width=self.bar_size)
            # self.ax_pe_doc.bar(n_doc+.5, F1, color=self.F1_color, width=self.bar_size)
            # self.ax_pe_doc.bar(n_doc - .5, precision, color=self.precision_color, width=self.bar_size)
            # self.ax_pe_doc.bar(n_doc, recall, color=self.recall_color, width=self.bar_size)
            self.ax_pe_doc.bar(n_doc, F1, color=self.F1_color, width=self.bar_size)

        self.ax_pe_doc.set_xlim(-1, n_doc + 1)
        self.ax_pe_doc.set_xticks([x for x in range(n_doc + 1)])
        self.ax_pe_doc.set_xticklabels(['{}\n{}'.format(doc[:5].strip(),
                                                        agreement.support_pe)
                                        for doc in self.doc_list])
        # self.ax_pe_doc.set_title('Document\nAgreement')
        self.ax_pe_doc.spines['top'].set_visible(False)
        self.ax_pe_doc.spines['right'].set_visible(False)
        # new helper method to auto-label bars
        for container in self.ax_pe_doc.containers:
            self.ax_pe_doc.bar_label(container)
        self.fig_pe_doc.tight_layout()
        self.canvas_pe_doc_plot.draw()
        self.canvas_pe_doc.update()

        # self.canvas_doc.draw()

    def DrawGraphsGlobal_pe(self, agreement):
        self.ax_pe_global.clear()
        self.ax_pe_global.bar(0, agreement.precision_pe, color=self.precision_color, width=self.bar_size)
        self.ax_pe_global.bar(1, agreement.recall_pe, color=self.recall_color, width=self.bar_size)
        self.ax_pe_global.bar(2, agreement.F1_pe, color=self.F1_color, width=self.bar_size)

        # ticks = self.ax_global.axes.get_xticks()
        self.ax_pe_global.set_xlim(-.5, 2.5)
        self.ax_pe_global.set_xticks([0, 1, 2])
        # self.ax_global.axes
        self.ax_pe_global.set_xticklabels(['{}\n{}'.format(pe, agreement.support_pe)
                                           for pe in ['precision', 'recall', 'F1 score']])
        # self.ax_pe_global.set_title('Overall Agreement')
        self.ax_pe_global.spines['top'].set_visible(False)
        self.ax_pe_global.spines['right'].set_visible(False)
        # new helper method to auto-label bars
        for container in self.ax_pe_global.containers:
            self.ax_pe_global.bar_label(container)
        self.fig_pe_global.tight_layout()
        self.canvas_pe_global_plot.draw()
        self.canvas_pe_global.update()

    def DrawGraphsGlobal_re(self, agreement):
        self.ax_re_global.clear()
        self.ax_re_global.bar(0, agreement.precision_re, color=self.precision_color, width=self.bar_size)
        self.ax_re_global.bar(1, agreement.recall_re, color=self.recall_color, width=self.bar_size)
        self.ax_re_global.bar(2, agreement.F1_re, color=self.F1_color, width=self.bar_size)

        # ticks = self.ax_global.axes.get_xticks()
        self.ax_re_global.set_xlim(-.5, 2.5)
        self.ax_re_global.set_xticks([0, 1, 2])
        # self.ax_global.axes
        self.ax_re_global.set_xticklabels(['{}\n{}'.format(re, agreement.support_re)
                                           for re in ['precision', 'recall', 'F1 score']])
        # self.ax_pe_global.set_title('Overall Agreement')
        self.ax_re_global.spines['top'].set_visible(False)
        self.ax_re_global.spines['right'].set_visible(False)
        # new helper method to auto-label bars
        for container in self.ax_re_global.containers:
            self.ax_re_global.bar_label(container)
        self.fig_re_global.tight_layout()
        self.canvas_re_global_plot.draw()
        self.canvas_re_global.update()

    def CalculateAgreementPe(self, *events):
        process_elements_list = list()

        if self.ACTIVITY_CHK.get():
            process_elements_list.append('Activity')
        if self.ACTIVITYDATA_CHK.get():
            process_elements_list.append('Activity Data')
        if self.ACTOR_CHK.get():
            process_elements_list.append('Actor')
        if self.GATEWAY_CHK.get():
            process_elements_list.append('XOR Gateway')
            process_elements_list.append('AND Gateway')
        if self.CONDITION_SPECIFICATION_CHK.get():
            process_elements_list.append('Condition Specification')
        if self.FURTHER_SPECIFICATION_CHK.get():
            process_elements_list.append('Further Specification')
        self.pe_selected_labels = process_elements_list

        self.doc_list = sorted([self.lst_documents.get(doc_id)
                                for doc_id in self.lst_documents.curselection()])
        annotator_name = self.lst_annotators.get(self.lst_annotators.curselection()[0])
        agreement = CalculateBaselinePredictorsF1(self.dataset,
                                                  self.doc_list,
                                                  annotator_name,
                                                  process_elements_list,
                                                  None)
        try:
            agreement.ComputeAgreement_pe()
            self.DrawGraphsPe(agreement=agreement)
        except:
            self.ax_pe_global.clear()
            self.ax_pe_global.set_title('No Token Classification baseline for this predictor')
            self.canvas_pe_global_plot.draw()
            self.canvas_pe_global.update()

    def CalculateAgreementRe(self, *events):
        relations_list = list()
        if self.RE_SEQUENCE_FLOW.get():
            relations_list.append('a4Flows')
        if self.RE_USES.get():
            relations_list.append('a2Uses')
        if self.RE_ROLES_PERFORMER.get():
            # relations_list.append('Roles')
            relations_list.append('Actor Performer')
        if self.RE_ROLES_RECIPIENT.get():
            relations_list.append('Actor Recipient')
        if self.RE_FURTHER_SPECIFICATION.get():
            relations_list.append('a5FurtherSpecification', )
        if self.RE_SAME_GATEWAY.get():
            relations_list.append('a6SameGateway')
        self.re_selected_labels = relations_list

        self.doc_list = sorted([self.lst_documents.get(doc_id)
                                for doc_id in self.lst_documents.curselection()])
        annotator_name = self.lst_annotators.get(self.lst_annotators.curselection()[0])
        agreement = CalculateBaselinePredictorsF1(self.dataset,
                                                  self.doc_list,
                                                  annotator_name,
                                                  None,
                                                  relations_list)
        try:
            agreement.ComputeAgreement_re()  # .ComputeAgreement()
            self.DrawGraphsRe(agreement=agreement)
        except:
            self.ax_re_global.clear()
            self.ax_re_global.set_title('No Relation Extraction baseline for this predictor')
            self.canvas_re_global_plot.draw()
            self.canvas_re_global.update()

    def DocumentsListChanged(self, *events):
        # print('DocumentChanged')
        # doc_names = list(self.dataset.dataset['documents'].keys())
        # selected_docs = list(self.lst_documents.curselection())
        self.document_list = sorted([self.lst_documents.get(item) for item in self.lst_documents.curselection()])
        # doc_names[index] for index in selected_docs])
        self.UpdateAnnotatorList()

    def UpdateAnnotatorList(self):
        # retrieve baseline predictor names
        annotators = list()
        for doc_name in self.document_list:
            annotators.extend(list(self.dataset.dataset['documents'][doc_name]['predictors'].keys()))
        annotators = list(set(annotators))
        self.lst_annotators.delete(0, 'end')
        for annotator in annotators:
            self.lst_annotators.insert(tk.END, annotator)
        self.annotator_list = annotators
        self.lst_annotators.select_set(0, 0)

    def LoadDocumentsList(self):
        self.lst_documents.delete(0, 'end')
        for doc in sorted(self.dataset.GetGoldStandardDocuments()):
            self.lst_documents.insert(tk.END, doc)
        # select all elements in annotators list
        # self.lst_documents.select_set(0,'end')
        self.DocumentsListChanged()

    def SelectAllDocuments(self,
                           *event):
        self.lst_documents.selection_set(0, 'end')
        self.DocumentsListChanged()

    def DeselectAllDocuments(self,
                             *event):
        self.lst_documents.select_clear(0, 'end')
        self.lst_documents.selection_set(0, 0)
        self.DocumentsListChanged()

    def CreateFrame(self):
        # frame
        self.Frame = tk.Frame(self.parent)
        self.Frame.pack(fill='both',
                        expand=True)

        self.frmCommands = tk.Frame(self.Frame)
        self.frmCommands.pack(fill='x')
        self.frmCommands.pack_propagate(0)

        self.btnOpenClose = tk.Button(self.frmCommands, textvariable=self.btnOpenCloseText,
                                      command=self.OpenClose)
        self.btnOpenClose.pack(side='left',
                               fill='y')

        frmlbl_ = tk.LabelFrame(self.frmCommands, text='Documents')
        frmlbl_.pack(
                side='left',
                fill='y',
                # expand=True
        )
        frmlbl_doc = tk.Frame(frmlbl_)
        frmlbl_doc.pack(
                # side='left',
                fill='both',
                expand=True
        )
        self.lst_documents = tk.Listbox(frmlbl_doc,
                                        selectmode='multiple',
                                        exportselection=False)
        self.lst_documents.pack(
                side='left',
                fill='y',
                # expand=True
        )
        scrollbar_doc = tk.Scrollbar(frmlbl_doc)
        scrollbar_doc.pack(side=tk.RIGHT, fill='y')
        self.lst_documents.config(yscrollcommand=scrollbar_doc.set)
        scrollbar_doc.config(command=self.lst_documents.yview)
        self.lst_documents.bind('<<ListboxSelect>>', self.DocumentsListChanged)
        tk.Button(frmlbl_,
                  text='select all documents',
                  command=self.SelectAllDocuments).pack(side='bottom',
                                                        fill='x')
        tk.Button(frmlbl_,
                  text='Deselect documents',
                  command=self.DeselectAllDocuments).pack(side='bottom',
                                                          fill='x')

        # LIST ANNOTATORS
        frmlbl_ = tk.LabelFrame(self.frmCommands, text='Annotators')
        frmlbl_.pack(
                side='left',
                fill='y',
                # expand=True
        )
        self.lst_annotators = tk.Listbox(frmlbl_,
                                         selectmode='single',
                                         exportselection=False)
        self.lst_annotators.pack(side='left',
                                 fill='x',
                                 expand=True
                                 )
        scrollbar_ann = tk.Scrollbar(frmlbl_)
        scrollbar_ann.pack(side=tk.RIGHT, fill='y')
        self.lst_annotators.config(yscrollcommand=scrollbar_ann.set)
        scrollbar_ann.config(command=self.lst_annotators.yview)

        ############ PROCESS ELEMENTS ######################
        frmlbl_pe = tk.LabelFrame(self.frmCommands, text='Process Elements')
        frmlbl_pe.pack(
                side='left',
                fill='y', )
        # ACTIVITY
        chkActivity = tk.Checkbutton(frmlbl_pe,
                                     text='Activity',
                                     variable=self.ACTIVITY_CHK,
                                     # command=self.UpdateFrame,
                                     background=MARK_COLORS['Activity'],
                                     # justify=tk.LEFT
                                     )
        chkActivity.pack(side='top',
                         anchor='w',
                         fill='x')

        # FURTHER SPECIFICATION
        chkFurtherSpecification = tk.Checkbutton(frmlbl_pe,
                                                 text='Further Specification',
                                                 variable=self.FURTHER_SPECIFICATION_CHK,
                                                 # command=self.UpdateFrame,
                                                 background=MARK_COLORS['Further Specification'],
                                                 )

        chkFurtherSpecification.pack(
                side='top',
                anchor='w',
                fill='x')

        chkActivityData = tk.Checkbutton(frmlbl_pe,
                                         text='Activity Data',
                                         variable=self.ACTIVITYDATA_CHK,
                                         # command=self.UpdateFrame,
                                         background=MARK_COLORS['Activity Data'],
                                         )
        chkActivityData.pack(side='top',
                             anchor='w',
                             fill='x')

        chkActor = tk.Checkbutton(frmlbl_pe,
                                  text='Actor',
                                  variable=self.ACTOR_CHK,
                                  # command=self.UpdateFrame,
                                  background=MARK_COLORS['Actor'],
                                  )
        chkActor.pack(side='top',
                      anchor='w',
                      fill='x')
        # GATEWAY
        chkGateway = tk.Checkbutton(frmlbl_pe,
                                    text='Gateway',
                                    variable=self.GATEWAY_CHK,
                                    # command=self.UpdateFrame,
                                    background=MARK_COLORS['XOR Gateway'],
                                    # justify=tk.LEFT
                                    )
        chkGateway.pack(side='top',
                        anchor='w',
                        fill='x')
        ToolTipGateways(chkGateway)

        chkConditionSpecification = tk.Checkbutton(frmlbl_pe,
                                                   text='Condition Specification',
                                                   variable=self.CONDITION_SPECIFICATION_CHK,
                                                   # command=self.UpdateFrame,
                                                   background=MARK_COLORS['Condition Specification'],
                                                   )
        chkConditionSpecification.pack(side='top',
                                       anchor='w',
                                       fill='x')

        ############ RELATIONS ######################
        frmlbl_re = tk.LabelFrame(self.frmCommands, text='Relations')
        frmlbl_re.pack(
                side='left',
                fill='y', )
        chkFlow = tk.Checkbutton(frmlbl_re,
                                 text='Behavioral.Sequence Flow',
                                 variable=self.RE_SEQUENCE_FLOW,
                                 # command=self.UpdateCheckBoxes,
                                 background=MARK_COLORS['Sequence Flow'],
                                 )
        chkFlow.pack(side='top', anchor='w', fill='x')

        chkFurtherSpecificationRelation = tk.Checkbutton(frmlbl_re,
                                                         text='Activity.Further Specification',
                                                         variable=self.RE_FURTHER_SPECIFICATION,
                                                         # command=self.UpdateCheckBoxes,
                                                         background=MARK_COLORS['Further Specification'],
                                                         )
        chkFurtherSpecificationRelation.pack(side='top', anchor='w', fill='x')

        chkUses = tk.Checkbutton(frmlbl_re,
                                 text='Activity.Uses',
                                 variable=self.RE_USES,
                                 # command=self.UpdateCheckBoxes,
                                 background=MARK_COLORS['Uses'],
                                 )
        chkUses.pack(side='top', anchor='w', fill='x')

        tk.Checkbutton(frmlbl_re,
                       text='Activity.Roles.Actor Performer',
                       variable=self.RE_ROLES_PERFORMER,
                       # command=self.UpdateCheckBoxes,
                       background=MARK_COLORS['Roles'],
                       ).pack(side='top', anchor='w', fill='x')
        tk.Checkbutton(frmlbl_re,
                       text='Activity.Roles.Actor Recipient',
                       variable=self.RE_ROLES_RECIPIENT,
                       # command=self.UpdateCheckBoxes,
                       background=MARK_COLORS['Roles'],
                       ).pack(side='top', anchor='w', fill='x')

        tk.Label(frmlbl_re, text='').pack(side='top')
        tk.Checkbutton(frmlbl_re,
                       text='Gateway.Same Gateway',
                       variable=self.RE_SAME_GATEWAY,
                       # command=self.UpdateCheckBoxes,
                       background=MARK_COLORS['Same Gateway'],
                       ).pack(side='top', anchor='w', fill='x')

        frm_calculate = tk.Frame(self.frmCommands)
        frm_calculate.pack(side='left', anchor='w', fill='x')
        tk.Button(frm_calculate,
                  text='Calculate Agreement Process elements',
                  command=self.CalculateAgreementPe,
                  background='azure',
                  ).pack(side='top', fill='both')

        tk.Button(frm_calculate,
                  text='Calculate Agreement Relations',
                  command=self.CalculateAgreementRe,
                  background='azure',
                  ).pack(side='top', fill='both')
        # tk.Button(frm_calculate,
        #           text = 'Calculate Agreement\n for all documents',
        #           command=self.Calculate_all,
        #           background='azure',
        #           ).pack(side='top', fill='both')
        # =============================================================================
        self.Expand()

        # =============================================================================
        #         # CANVAS FOR FIGURES
        # =============================================================================
        lblF1 = tk.Label(self.Frame,
                         textvariable=self.F1,
                         bg='green')
        lblF1.pack(side=tk.BOTTOM,
                   fill='x')
        #
        frm_figs = tk.Frame(self.Frame)
        frm_figs.pack(
                # side='top',
                fill='both',
                expand=True)
        #
        # tk.Button(frm_figs,
        #           text='Export Figures',
        #           command=self.ExportFigures).pack()

        self.notebook = ttk.Notebook(frm_figs)
        self.notebook.pack(fill='both', expand=True)

        #  PE
        self.notebook_pe = ttk.Notebook(self.notebook)
        self.notebook_pe.pack(fill='both', expand=True)

        frm_pe_global = tk.Frame(self.notebook_pe)
        frm_pe_global.pack(fill='both', expand=True)
        self.canvas_pe_global = tk.Canvas(frm_pe_global)
        self.canvas_pe_global.pack(fill='both', expand=True)
        self.canvas_pe_global_plot = FigureCanvasTkAgg(self.fig_pe_global, master=self.canvas_pe_global)
        self.canvas_pe_global_plot.get_tk_widget().pack(
                fill='both',
                expand=1)
        self.notebook_pe.add(frm_pe_global, text='Overall Agreement')
        ToolTipLegend(self.canvas_pe_global)

        frm_pe_doc = tk.Frame(self.notebook_pe)
        frm_pe_doc.pack(fill='both', expand=True)
        self.canvas_pe_doc = tk.Canvas(frm_pe_doc)
        self.canvas_pe_doc.pack(fill='both', expand=True)

        self.canvas_pe_doc_plot = FigureCanvasTkAgg(self.fig_pe_doc,
                                                    master=self.canvas_pe_doc)  # self.canvas)  # A tk.DrawingArea.
        self.canvas_pe_doc_plot.get_tk_widget().pack(
                fill='both',
                expand=1)
        self.notebook_pe.add(frm_pe_doc, text='Document Agreement')
        ToolTipLegend(self.canvas_pe_doc)

        frm_pe_pe = tk.Frame(self.notebook_pe)
        frm_pe_pe.pack(
                # side='left',
                fill='both',
                expand=True)
        self.canvas_pe_pe = tk.Canvas(frm_pe_pe)
        self.canvas_pe_pe.pack(fill='both', expand=True)
        self.canvas_pe_pe_plot = FigureCanvasTkAgg(self.fig_pe_pe, master=self.canvas_pe_pe)
        self.canvas_pe_pe_plot.get_tk_widget().pack(
                fill='both',
                expand=1)
        self.notebook_pe.add(frm_pe_pe, text='Process Elements Agreement')
        ToolTipLegend(self.canvas_pe_pe)

        self.notebook.add(self.notebook_pe, text='Process Elements')

        # RE
        self.notebook_re = ttk.Notebook(self.notebook)
        self.notebook_re.pack(fill='both', expand=True)

        frm_re_global = tk.Frame(self.notebook_re)
        frm_re_global.pack(fill='both', expand=True)
        self.canvas_re_global = tk.Canvas(frm_re_global)
        self.canvas_re_global.pack(fill='both', expand=True)
        self.canvas_re_global_plot = FigureCanvasTkAgg(self.fig_re_global, master=self.canvas_re_global)
        self.canvas_re_global_plot.get_tk_widget().pack(
                fill='both',
                expand=1)
        self.notebook_re.add(frm_re_global, text='Overall Agreement')
        ToolTipLegend(self.canvas_re_global)

        frm_re_doc = tk.Frame(self.notebook_re)
        frm_re_doc.pack(fill='both', expand=True)
        self.canvas_re_doc = tk.Canvas(frm_re_doc)
        self.canvas_re_doc.pack(fill='both', expand=True)

        self.canvas_re_doc_plot = FigureCanvasTkAgg(self.fig_re_doc,
                                                    master=self.canvas_re_doc)  # self.canvas)  # A tk.DrawingArea.
        self.canvas_re_doc_plot.get_tk_widget().pack(
                fill='both',
                expand=1)
        self.notebook_re.add(frm_re_doc, text='Document Agreement')
        ToolTipLegend(self.canvas_re_doc)

        frm_re_pe = tk.Frame(self.notebook_re)
        frm_re_pe.pack(
                # side='left',
                fill='both',
                expand=True)
        self.canvas_re_re = tk.Canvas(frm_re_pe)
        self.canvas_re_re.pack(fill='both', expand=True)
        self.canvas_re_re_plot = FigureCanvasTkAgg(self.fig_re_re, master=self.canvas_re_re)
        self.canvas_re_re_plot.get_tk_widget().pack(
                fill='both',
                expand=1)
        self.notebook_re.add(frm_re_pe, text='Relation Type Agreement')

        self.notebook.add(self.notebook_re, text='Relations')
        ToolTipLegend(self.canvas_re_re)

        # frm_export_figs = tk.Frame(self.notebook)
        # frm_export_figs.pack(fill='both', expand=True)
        #
        # self.notebook.add(self.notebook_re, text='Export Figures')

    
    def OpenClose(self):
        if self.btnOpenCloseStatus.get():
            self.Close()
        else:
            self.Expand()

    def Close(self):
        self.frmCommands.config(height=self.width_closed)
        # self.Frame.config(height=self.parent.winfo_height())
        self.btnOpenCloseText.set('Open \nCommands')
        self.btnOpenCloseStatus.set(False)
        # print('navi closed')

    def Expand(self):
        self.frmCommands.config(height=self.width_expanded)
        # self.Frame.config(height=self.parent.winfo_height())
        self.btnOpenCloseText.set('Close \nCommands')
        self.btnOpenCloseStatus.set(True)
        # print('navi opened')

    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            self.canvas_global.xview_scroll(scroll, "units")
        else:
            self.canvas_global.yview_scroll(scroll, "units")

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
    getdata()
    curdir = Path(os.path.curdir).absolute()
    curdir = curdir.joinpath('petdatasetgoldstandardbaselines.json')
    # print(curdir.absolute())
    dataset_filename = curdir.absolute()
    dataset = AnnotationDataset()
    dataset.LoadDataset(filename=dataset_filename)

    window = tk.Tk()
    # window.geometry('950x600')
    program = F1BaselinePredictorsAgreement(window, dataset)
    # Start the GUI event loop
    program.mainloop()

if __name__ == '__main__':
    
    Show()
    