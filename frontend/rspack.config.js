import path from 'path';
import { fileURLToPath } from 'url';
import rspack from '@rspack/core';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default {
  entry: {
    main: './src/index.jsx',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    clean: true,
  },
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'builtin:swc-loader',
          options: {
            jsc: {
              parser: {
                syntax: 'ecmascript',
                jsx: true,
              },
              transform: {
                react: {
                  runtime: 'automatic',
                },
              },
            },
          },
        },
      },
      {
        test: /\.css$/,
        // Use CssExtractRspackPlugin.loader instead of style-loader to prevent flicker
        use: [rspack.CssExtractRspackPlugin.loader, 'css-loader'],
        type: 'javascript/auto',
      },
    ],
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'react',
          chunks: 'all',
          priority: 10,
        },
      },
    },
    minimize: true,
  },
  plugins: [
    new rspack.HtmlRspackPlugin({
      template: './public/index.html',
    }),
    // Extracts CSS into a separate file for instant loading
    new rspack.CssExtractRspackPlugin({
      filename: '[name].css',
    }),
  ],
  devServer: {
    port: 3001,
    hot: true,
  },
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
};
