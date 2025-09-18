import React, { useState } from 'react';
import { Upload, File, X, FileCheck, Cloud } from 'lucide-react';

const FileUploader = ({ onFileSelect, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFile = (file) => {
    console.log('=== FILE SELECTED ===');
    console.log('File object:', file);
    console.log('File name:', file.name);
    console.log('File size:', file.size);
    console.log('File type:', file.type);
    console.log('File last modified:', file.lastModified);
    
    if (file.type === 'application/pdf') {
      setSelectedFile(file);
      onFileSelect(file);
    } else {
      console.error('Invalid file type:', file.type);
      alert('Please select a PDF file');
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    onFileSelect(null);
  };

  return (
    <div className="w-full">
      <div
        className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${
          dragActive
            ? 'border-azure bg-charcoal/60 scale-105'
            : selectedFile
            ? 'border-green-300 bg-green-50'
            : 'border-gray-300 hover:border-azure hover:bg-midnight/40'
        } ${isLoading ? 'opacity-50 pointer-events-none' : ''} text-white`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {isLoading && (
          <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-xl">
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-2 text-sm text-gray-600">Analyzing contract...</p>
            </div>
          </div>
        )}

        {selectedFile ? (
          <div className="flex items-center justify-between p-4 bg-white rounded-lg border border-green-200 shadow-sm">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <FileCheck className="w-8 h-8 text-green-600" />
              </div>
              <div className="text-left">
                <p className="font-semibold text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB • PDF Document
                </p>
                <div className="flex items-center space-x-1 mt-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-xs text-green-600 font-medium">Ready for analysis</span>
                </div>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="p-2 hover:bg-red-100 rounded-lg transition-colors group"
              disabled={isLoading}
              title="Remove file"
            >
              <X className="w-5 h-5 text-gray-400 group-hover:text-red-500" />
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex justify-center">
              <div className="p-4 bg-blue-100 rounded-full">
                <Upload className="h-12 w-12 text-blue-600" />
              </div>
            </div>
            
            <div>
              <p className="text-lg font-semibold text-white-900 mb-2">
                Upload your contract
              </p>
              <p className="text-sm text-white-600 mb-4">
                Drag and drop your PDF contract here, or click to browse
              </p>
              
              <label htmlFor="file-upload" className="inline-flex items-center px-6 py-3 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors cursor-pointer">
                <Cloud className="w-4 h-4 mr-2" />
                Choose File
                <input
                  id="file-upload"
                  name="file-upload"
                  type="file"
                  className="sr-only"
                  accept=".pdf"
                  onChange={(e) => e.target.files[0] && handleFile(e.target.files[0])}
                />
              </label>
            </div>
            
            <div className="pt-4 border-t border-gray-200">
              <div className="flex items-center justify-center space-x-6 text-xs text-gray-500">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>PDF files only</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <span>Max 10MB</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                  <span>Secure upload</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUploader;