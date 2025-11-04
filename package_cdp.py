#!/usr/bin/env python3
"""Package Certification Data Package (CDP) for external audit.

This script packages all QuASIM certification artifacts into a structured
ZIP file ready for submission to NASA SMA and SpaceX GNC teams.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


class CDPPackager:
    """Package certification artifacts for external audit."""

    def __init__(self, version: str = "1.0", output_dir: str = "."):
        """Initialize packager.

        Args:
            version: CDP version number
            output_dir: Output directory for package
        """
        self.version = version
        self.output_dir = Path(output_dir)
        self.package_name = f"CDP_v{version}"

    def collect_artifacts(self) -> dict[str, Path]:
        """Collect all required certification artifacts.

        Returns:
            Dictionary mapping artifact names to their paths
        """
        artifacts = {}
        base_path = Path(".")

        # Core CDP artifacts
        cdp_artifacts = [
            "cdp_artifacts/CDP_v1.0.json",
            "cdp_artifacts/traceability_matrix.csv",
            "cdp_artifacts/audit_checklist.md",
            "cdp_artifacts/review_schedule.md",
            "cdp_artifacts/README.md",
        ]

        # Monte Carlo and verification artifacts
        verification_artifacts = [
            "montecarlo_campaigns/MC_Results_1024.json",
            "montecarlo_campaigns/coverage_matrix.csv",
            "seed_management/seed_audit.log",
        ]

        all_artifact_paths = cdp_artifacts + verification_artifacts

        for artifact_path in all_artifact_paths:
            full_path = base_path / artifact_path
            if full_path.exists():
                artifacts[artifact_path] = full_path
            else:
                print(f"⚠ Warning: Artifact not found: {artifact_path}")

        return artifacts

    def create_package_manifest(self, artifacts: dict[str, Path]) -> dict:
        """Create package manifest with metadata.

        Args:
            artifacts: Dictionary of collected artifacts

        Returns:
            Manifest dictionary
        """
        manifest = {
            "package": {
                "name": self.package_name,
                "version": self.version,
                "created": datetime.now().isoformat(),
                "document_id": "QA-SIM-INT-90D-RDMP-001",
            },
            "standards": [
                "DO-178C Level A",
                "ECSS-Q-ST-80C Rev. 2",
                "NASA E-HBK-4008",
            ],
            "partners": ["SpaceX", "NASA SMA"],
            "status": "READY_FOR_AUDIT",
            "artifacts": [],
        }

        for artifact_name, artifact_path in artifacts.items():
            stat = artifact_path.stat()
            manifest["artifacts"].append({
                "name": artifact_name,
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })

        return manifest

    def package_artifacts(self, output_path: Path | None = None) -> str:
        """Package all artifacts into a ZIP file.

        Args:
            output_path: Optional custom output path

        Returns:
            Path to created package
        """
        if output_path is None:
            output_path = self.output_dir / f"{self.package_name}.zip"

        print(f"\n{'=' * 70}")
        print(f"QuASIM Certification Data Package - Packaging")
        print(f"Version: {self.version}")
        print(f"{'=' * 70}\n")

        # Collect artifacts
        print("Collecting artifacts...")
        artifacts = self.collect_artifacts()
        print(f"✓ Collected {len(artifacts)} artifacts\n")

        # Create manifest
        print("Creating package manifest...")
        manifest = self.create_package_manifest(artifacts)

        # Create temporary manifest file
        manifest_path = Path("/tmp/CDP_MANIFEST.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        # Create ZIP package
        print(f"Creating package: {output_path}")
        with ZipFile(output_path, "w", ZIP_DEFLATED) as zipf:
            # Add manifest
            zipf.write(manifest_path, "CDP_MANIFEST.json")

            # Add all artifacts
            for artifact_name, artifact_path in artifacts.items():
                zipf.write(artifact_path, artifact_name)
                print(f"  + {artifact_name}")

        # Clean up temporary manifest
        manifest_path.unlink()

        # Print summary
        package_size = output_path.stat().st_size
        print(f"\n{'=' * 70}")
        print(f"✓ Package created successfully")
        print(f"  Path: {output_path}")
        print(f"  Size: {package_size:,} bytes ({package_size / 1024:.1f} KB)")
        print(f"  Artifacts: {len(artifacts)}")
        print(f"{'=' * 70}\n")

        return str(output_path)

    def validate_package(self, package_path: Path) -> bool:
        """Validate the created package.

        Args:
            package_path: Path to package ZIP file

        Returns:
            True if package is valid
        """
        print("Validating package...")

        try:
            with ZipFile(package_path, "r") as zipf:
                # Check manifest exists
                if "CDP_MANIFEST.json" not in zipf.namelist():
                    print("✗ Manifest not found in package")
                    return False

                # Validate manifest
                with zipf.open("CDP_MANIFEST.json") as f:
                    manifest = json.load(f)

                expected_artifacts = len(manifest["artifacts"])
                actual_artifacts = len(zipf.namelist()) - 1  # Exclude manifest

                if expected_artifacts != actual_artifacts:
                    print(f"✗ Artifact count mismatch: expected {expected_artifacts}, found {actual_artifacts}")
                    return False

                # Check for required artifacts
                required = [
                    "cdp_artifacts/CDP_v1.0.json",
                    "cdp_artifacts/traceability_matrix.csv",
                    "cdp_artifacts/audit_checklist.md",
                    "montecarlo_campaigns/MC_Results_1024.json",
                ]

                for req_artifact in required:
                    if req_artifact not in zipf.namelist():
                        print(f"✗ Required artifact missing: {req_artifact}")
                        return False

                print(f"✓ Package validation passed")
                print(f"  Manifest: Valid")
                print(f"  Artifacts: {actual_artifacts}/{expected_artifacts}")
                print(f"  Required artifacts: Present")
                return True

        except Exception as e:
            print(f"✗ Validation failed: {e}")
            return False

    def create_submission_readme(self) -> str:
        """Create a submission README for external reviewers.

        Returns:
            Path to created README
        """
        readme_content = f"""# QuASIM Certification Data Package v{self.version}

## Submission Information

- **Package**: {self.package_name}.zip
- **Version**: {self.version}
- **Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Document ID**: QA-SIM-INT-90D-RDMP-001
- **Organization**: QuASIM
- **Status**: READY_FOR_AUDIT

## For External Reviewers

This package contains the complete Certification Data Package for QuASIM, prepared in accordance with:
- DO-178C Level A
- ECSS-Q-ST-80C Rev. 2
- NASA E-HBK-4008

### Package Contents

Extract the ZIP file to access:

1. **CDP_MANIFEST.json** - Package manifest and metadata
2. **cdp_artifacts/** - Core certification documentation
   - CDP_v1.0.json - Certification metadata
   - traceability_matrix.csv - Requirements traceability
   - audit_checklist.md - Comprehensive audit checklist
   - review_schedule.md - Review coordination plan
   - README.md - Detailed package documentation
3. **montecarlo_campaigns/** - Simulation verification evidence
   - MC_Results_1024.json - Fidelity analysis
   - coverage_matrix.csv - MC/DC coverage
4. **seed_management/** - Determinism verification
   - seed_audit.log - Replay validation

### Quick Start

1. Extract {self.package_name}.zip
2. Review CDP_MANIFEST.json for package contents
3. Read cdp_artifacts/README.md for detailed documentation
4. Follow cdp_artifacts/review_schedule.md for review process

### Contact

For questions or clarifications:
- Email: quasim-cdp@example.com
- Subject: CDP v{self.version} Review

### Review Timeline

- **Week 1**: Initial package review
- **Week 2**: Technical deep-dive
- **Week 3**: Final sign-off

See cdp_artifacts/review_schedule.md for detailed agenda and participant information.

---
*Prepared for NASA SMA and SpaceX GNC review teams*
"""

        output_path = self.output_dir / "CDP_SUBMISSION_README.md"
        with open(output_path, "w") as f:
            f.write(readme_content)

        print(f"✓ Created submission README: {output_path}")
        return str(output_path)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Package QuASIM Certification Data Package for external audit"
    )
    parser.add_argument(
        "--version",
        default="1.0",
        help="CDP version number (default: 1.0)",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory for package (default: current directory)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate package after creation",
    )

    args = parser.parse_args()

    packager = CDPPackager(version=args.version, output_dir=args.output_dir)

    # Create package
    package_path = packager.package_artifacts()

    # Validate if requested
    if args.validate:
        print()
        if not packager.validate_package(Path(package_path)):
            print("\n⚠ Package validation failed!")
            return 1

    # Create submission README
    print()
    packager.create_submission_readme()

    print("\n✓ CDP packaging complete - ready for external audit submission")
    return 0


if __name__ == "__main__":
    exit(main())
