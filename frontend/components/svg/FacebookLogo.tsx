interface FacebookLogoProps {
  width?: number;
  height?: number;
  fill?: string;
}

const FacebookLogo = ({ width = 7, height = 15, fill = '#F4F4F4' }: FacebookLogoProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 7 15"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M1.55073 15V7.49941H0V4.91457H1.55073V3.36264C1.55073 1.25393 2.42638 0 4.91418 0H6.98534V2.58514H5.69072C4.72228 2.58514 4.65821 2.94637 4.65821 3.62054L4.65469 4.91428H7L6.72556 7.49912H4.65469V15H1.55073Z"
        fill={fill}
      />
    </svg>
  );
};

export default FacebookLogo;
