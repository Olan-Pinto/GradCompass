import { create } from 'zustand';
import axios from 'axios';
import toast from 'react-hot-toast';

export const useFinanceStore = create((set, get) => ({
  loading: false,
  error: null,
  researchResult: null,
  tuitionResult: null,
  livingCostResult: null,
  fundingResult: null,
  
  // Research comprehensive financial plan
  researchComprehensive: async (params) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post('/cost-research/comprehensive', params);
      set({ 
        researchResult: response.data.data,
        tuitionResult: response.data.data.tuition_research?.data,
        livingCostResult: response.data.data.living_cost_research?.data,
        fundingResult: response.data.data.funding_research?.data,
        loading: false 
      });
      toast.success('Financial blueprint generated successfully!');
      return { success: true, data: response.data.data };
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to research costs';
      set({ error: message, loading: false });
      toast.error(message);
      return { success: false, error: message };
    }
  },

  // Research individual components if needed
  researchTuition: async (params) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post('/cost-research/tuition', params);
      set({ tuitionResult: response.data.data, loading: false });
      return { success: true, data: response.data.data };
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to research tuition';
      set({ error: message, loading: false });
      toast.error(message);
      return { success: false, error: message };
    }
  },

  researchLivingCosts: async (params) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post('/cost-research/cost-of-living', params);
      set({ livingCostResult: response.data.data, loading: false });
      return { success: true, data: response.data.data };
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to research living costs';
      set({ error: message, loading: false });
      toast.error(message);
      return { success: false, error: message };
    }
  },

  researchFunding: async (params) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post('/cost-research/funding', params);
      set({ fundingResult: response.data.data, loading: false });
      return { success: true, data: response.data.data };
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to research funding';
      set({ error: message, loading: false });
      toast.error(message);
      return { success: false, error: message };
    }
  },

  clearResults: () => {
    set({ 
      researchResult: null, 
      tuitionResult: null, 
      livingCostResult: null, 
      fundingResult: null,
      error: null 
    });
  }
}));
