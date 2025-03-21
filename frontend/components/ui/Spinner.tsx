"use client";

import dynamic from "next/dynamic";
import { FC } from "react";

const Lottie = dynamic(() => import("lottie-react"), { ssr: false });
import animation from "@/assets/loading-anim.json";

const Spinner: FC = () => (
  <Lottie
    animationData={animation}
    style={{
      width: 240,
      height: 240,
    }}
    loop={true}
  />
);

export default Spinner;
