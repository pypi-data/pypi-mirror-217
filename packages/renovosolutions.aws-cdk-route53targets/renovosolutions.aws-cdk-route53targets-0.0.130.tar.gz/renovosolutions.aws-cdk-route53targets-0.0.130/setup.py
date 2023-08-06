import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "renovosolutions.aws-cdk-route53targets",
    "version": "0.0.130",
    "description": "An AWS CDK library that adds functionality for targetting additional resources in Route53",
    "license": "Apache-2.0",
    "url": "https://github.com/RenovoSolutions/cdk-library-route53targets.git",
    "long_description_content_type": "text/markdown",
    "author": "Renovo Solutions<devops@renovo1.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/RenovoSolutions/cdk-library-route53targets.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "route53targets",
        "route53targets._jsii"
    ],
    "package_data": {
        "route53targets._jsii": [
            "cdk-library-route53targets@0.0.130.jsii.tgz"
        ],
        "route53targets": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.81.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.82.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
