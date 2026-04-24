use serde::{Serialize, Deserialize};
use walkdir::WalkDir;
use std::env;
use std::path::Path;
use std::fs;

#[derive(Serialize, Deserialize, Debug)]
struct FileInfo {
    path: String,
    size: u64,
}

#[derive(Serialize, Deserialize, Debug)]
struct AnalysisResult {
    total_files: usize,
    total_size: u64,
    largest_files: Vec<FileInfo>,
    error: Option<String>,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        let err = AnalysisResult {
            total_files: 0,
            total_size: 0,
            largest_files: vec![],
            error: Some("Missing directory path argument".to_string()),
        };
        println!("{}", serde_json::to_string(&err).unwrap());
        std::process::exit(1);
    }

    let root_path = &args[1];
    let mut total_files = 0;
    let mut total_size = 0;
    let mut files = Vec::new();

    for entry in WalkDir::new(root_path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            if let Ok(metadata) = entry.metadata() {
                let size = metadata.len();
                total_files += 1;
                total_size += size;
                files.push(FileInfo {
                    path: entry.path().to_string_lossy().into_owned(),
                    size,
                });
            }
        }
    }

    // Sort files by size descending and take top 5
    files.sort_by(|a, b| b.size.cmp(&a.size));
    let largest_files = files.into_iter().take(5).collect();

    let result = AnalysisResult {
        total_files,
        total_size,
        largest_files,
        error: None,
    };

    println!("{}", serde_json::to_string(&result).unwrap());
}
