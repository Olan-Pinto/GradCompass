import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  CurrencyDollarIcon, 
  ArrowLeftIcon, 
  ChatBubbleBottomCenterTextIcon,
  AcademicCapIcon,
  GlobeAltIcon,
  BanknotesIcon,
  DocumentTextIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import { useFinanceStore } from '../stores/financeStore';
import { useThemeStore } from '../stores/themeStore';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import MarkdownRenderer from '../components/ui/MarkdownRenderer';

function FinancePlannerPage() {
  const navigate = useNavigate();
  const { theme } = useThemeStore();
  const { 
    researchComprehensive, 
    loading, 
    researchResult, 
    clearResults 
  } = useFinanceStore();

  const [formData, setFormData] = useState({
    city: '',
    university_name: '',
    destination_country: 'USA'
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.city) return;
    await researchComprehensive(formData);
  };

  const handleReset = () => {
    clearResults();
    setFormData({
      city: '',
      university_name: '',
      destination_country: 'USA'
    });
  };

  const renderSafeContent = (content) => {
    if (!content) return null;
    if (typeof content === 'string') return content;
    if (Array.isArray(content)) {
      return content.map((item, i) => (
        <React.Fragment key={i}>
          {renderSafeContent(item)}
        </React.Fragment>
      ));
    }
    if (typeof content === 'object') {
      return content.text || content.content || JSON.stringify(content);
    }
    return String(content);
  };

  return (
    <div className={`min-h-screen pb-20 ${
      theme === 'dark' ? 'bg-mocha-base' : 'bg-latte-base'
    }`}>
      {/* Header */}
      <div className={`sticky top-0 z-10 border-b backdrop-blur-lg ${
        theme === 'dark' 
          ? 'bg-mocha-base/90 border-mocha-surface1/30' 
          : 'bg-latte-base/90 border-latte-surface1/30'
      }`}>
        <div className="max-w-5xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className={`p-2 rounded-lg transition-colors ${
                theme === 'dark'
                  ? 'hover:bg-mocha-surface0 text-mocha-subtext1 hover:text-mocha-text'
                  : 'hover:bg-latte-surface0 text-latte-subtext1 hover:text-latte-text'
              }`}
            >
              <ArrowLeftIcon className="w-5 h-5" />
            </button>
            
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg bg-gradient-to-br from-mocha-peach to-mocha-yellow`}>
                <CurrencyDollarIcon className="w-6 h-6 text-white" />
              </div>
              <h1 className={`text-2xl font-display font-bold ${
                theme === 'dark' ? 'text-mocha-text' : 'text-latte-text'
              }`}>
                Finance Planner
              </h1>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-8">
        {!researchResult ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-2xl mx-auto"
          >
            <div className={`rounded-2xl p-8 border backdrop-blur-sm ${
              theme === 'dark' 
                ? 'bg-mocha-surface0/50 border-mocha-surface1/30' 
                : 'bg-latte-surface0/50 border-latte-surface1/30'
            }`}>
              <div className="text-center mb-8">
                <SparklesIcon className={`w-12 h-12 mx-auto mb-4 ${
                  theme === 'dark' ? 'text-mocha-peach' : 'text-latte-peach'
                }`} />
                <h2 className={`text-2xl font-bold mb-2 ${
                  theme === 'dark' ? 'text-mocha-text' : 'text-latte-text'
                }`}>
                  Generate Your Financial Blueprint
                </h2>
                <p className={`${
                  theme === 'dark' ? 'text-mocha-subtext0' : 'text-latte-subtext0'
                }`}>
                  Research tuition, living costs, and funding options for your study abroad journey.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    theme === 'dark' ? 'text-mocha-subtext1' : 'text-latte-subtext1'
                  }`}>
                    Target City *
                  </label>
                  <input
                    type="text"
                    name="city"
                    required
                    value={formData.city}
                    onChange={handleInputChange}
                    placeholder="e.g. New York, Boston, London"
                    className={`w-full px-4 py-3 rounded-xl border transition-colors ${
                      theme === 'dark'
                        ? 'bg-mocha-surface1 border-mocha-surface2 text-mocha-text placeholder-mocha-subtext1 focus:border-mocha-peach focus:ring-2 focus:ring-mocha-peach/20'
                        : 'bg-latte-surface1 border-latte-surface2 text-latte-text placeholder-latte-subtext1 focus:border-latte-peach focus:ring-2 focus:ring-latte-peach/20'
                    } focus:outline-none`}
                  />
                </div>

                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    theme === 'dark' ? 'text-mocha-subtext1' : 'text-latte-subtext1'
                  }`}>
                    University Name (Optional)
                  </label>
                  <input
                    type="text"
                    name="university_name"
                    value={formData.university_name}
                    onChange={handleInputChange}
                    placeholder="e.g. Northeastern University"
                    className={`w-full px-4 py-3 rounded-xl border transition-colors ${
                      theme === 'dark'
                        ? 'bg-mocha-surface1 border-mocha-surface2 text-mocha-text placeholder-mocha-subtext1 focus:border-mocha-peach focus:ring-2 focus:ring-mocha-peach/20'
                        : 'bg-latte-surface1 border-latte-surface2 text-latte-text placeholder-latte-subtext1 focus:border-latte-peach focus:ring-2 focus:ring-latte-peach/20'
                    } focus:outline-none`}
                  />
                </div>

                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    theme === 'dark' ? 'text-mocha-subtext1' : 'text-latte-subtext1'
                  }`}>
                    Destination Country
                  </label>
                  <select
                    name="destination_country"
                    value={formData.destination_country}
                    onChange={handleInputChange}
                    className={`w-full px-4 py-3 rounded-xl border transition-colors ${
                      theme === 'dark'
                        ? 'bg-mocha-surface1 border-mocha-surface2 text-mocha-text focus:border-mocha-peach focus:ring-2 focus:ring-mocha-peach/20'
                        : 'bg-latte-surface1 border-latte-surface2 text-latte-text focus:border-latte-peach focus:ring-2 focus:ring-latte-peach/20'
                    } focus:outline-none`}
                  >
                    <option value="USA">United States (USA)</option>
                    <option value="CAN">Canada (CAN)</option>
                    <option value="GBR">United Kingdom (GBR)</option>
                    <option value="AUS">Australia (AUS)</option>
                    <option value="DEU">Germany (DEU)</option>
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={loading || !formData.city}
                  className={`w-full py-4 rounded-xl font-bold text-white transition-all duration-300 shadow-lg ${
                    loading 
                      ? 'bg-mocha-surface2 cursor-not-allowed' 
                      : 'bg-gradient-to-r from-mocha-peach to-mocha-yellow hover:scale-[1.02] active:scale-[0.98]'
                  }`}
                >
                  {loading ? (
                    <div className="flex items-center justify-center gap-3">
                      <LoadingSpinner size="sm" />
                      <span>Researching costs...</span>
                    </div>
                  ) : (
                    "Generate Comprehensive Plan"
                  )}
                </button>
              </form>
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-8"
          >
            <div className="flex items-center justify-between">
              <h2 className={`text-2xl font-bold ${
                theme === 'dark' ? 'text-mocha-text' : 'text-latte-text'
              }`}>
                Your Financial Blueprint for {formData.city}
              </h2>
              <button
                onClick={handleReset}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  theme === 'dark'
                    ? 'bg-mocha-surface0 hover:bg-mocha-surface1 text-mocha-text'
                    : 'bg-latte-surface0 hover:bg-latte-surface1 text-latte-text'
                }`}
              >
                Start New Research
              </button>
            </div>

            {/* Results Display */}
            <div className="grid gap-8">
              {/* Comprehensive Plan Section */}
              <div className={`p-8 rounded-2xl border ${
                theme === 'dark' 
                  ? 'bg-mocha-surface0/30 border-mocha-surface1/30' 
                  : 'bg-latte-surface0/30 border-latte-surface1/30'
              }`}>
                <div className="flex items-center gap-3 mb-6">
                  <ChatBubbleBottomCenterTextIcon className={`w-6 h-6 ${
                    theme === 'dark' ? 'text-mocha-peach' : 'text-latte-peach'
                  }`} />
                  <h3 className={`text-xl font-bold ${
                    theme === 'dark' ? 'text-mocha-text' : 'text-latte-text'
                  }`}>
                    Comprehensive Analysis
                  </h3>
                </div>
                <div className="prose-container">
                  <MarkdownRenderer content={researchResult.comprehensive_plan} />
                </div>
              </div>

              {/* Individual Details Grid */}
              <div className="grid md:grid-cols-2 gap-8">
                {/* Tuition */}
                <div className={`p-6 rounded-2xl border ${
                  theme === 'dark' ? 'bg-mocha-surface0/20 border-mocha-surface1/20' : 'bg-latte-surface0/20 border-latte-surface1/20'
                }`}>
                  <div className="flex items-center gap-3 mb-4">
                    <AcademicCapIcon className="w-5 h-5 text-mocha-blue" />
                    <h4 className="font-bold">Tuition Details</h4>
                  </div>
                  <div className="text-sm max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                    <MarkdownRenderer content={researchResult.tuition_research?.data} />
                  </div>
                </div>

                {/* Living Costs */}
                <div className={`p-6 rounded-2xl border ${
                  theme === 'dark' ? 'bg-mocha-surface0/20 border-mocha-surface1/20' : 'bg-latte-surface0/20 border-latte-surface1/20'
                }`}>
                  <div className="flex items-center gap-3 mb-4">
                    <GlobeAltIcon className="w-5 h-5 text-mocha-green" />
                    <h4 className="font-bold">Cost of Living</h4>
                  </div>
                  <div className="text-sm max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                    <MarkdownRenderer content={researchResult.living_cost_research?.data} />
                  </div>
                </div>

                {/* Funding */}
                <div className={`p-6 rounded-2xl border md:col-span-2 ${
                  theme === 'dark' ? 'bg-mocha-surface0/20 border-mocha-surface1/20' : 'bg-latte-surface0/20 border-latte-surface1/20'
                }`}>
                  <div className="flex items-center gap-3 mb-4">
                    <BanknotesIcon className="w-5 h-5 text-mocha-yellow" />
                    <h4 className="font-bold">Funding Options (Indian Institutions)</h4>
                  </div>
                  <div className="text-sm max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                    <MarkdownRenderer content={researchResult.funding_research?.data} />
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default FinancePlannerPage;
