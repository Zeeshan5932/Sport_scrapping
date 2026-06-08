declare module "*.css";
declare module "*.scss";
declare module "*.module.css";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
}

export {};
