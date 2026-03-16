import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MarkdownRenderer = ({ content, className = '' }) => {
  // If content is an object (from the previous bug), stringify it or take text
  const safeContent = typeof content === 'string' 
    ? content 
    : (content?.text || content?.content || JSON.stringify(content) || '');

  return (
    <div className={`prose prose-sm md:prose-base max-w-none dark:prose-invert 
      prose-headings:font-display prose-headings:font-bold 
      prose-p:leading-relaxed prose-p:text-mocha-text dark:prose-p:text-mocha-text
      prose-strong:text-mocha-mauve dark:prose-strong:text-mocha-mauve
      prose-a:text-mocha-blue hover:prose-a:text-mocha-sapphire
      prose-code:bg-mocha-surface0 prose-code:px-1 prose-code:rounded
      ${className}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {safeContent}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
