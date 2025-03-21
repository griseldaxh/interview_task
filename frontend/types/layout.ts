import { ReactNode } from "react";

export interface LayoutProps {
  children: ReactNode;
}

export interface MetadataConfig {
  title: string;
  description: string;
  icons: {
    icon: Array<{
      url: string;
      sizes?: string;
      type?: string;
    }>;
  };
}
