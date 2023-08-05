'''
<img src="https://raw.githubusercontent.com/mrgrain/cdk-esbuild/main/images/wordmark.svg" alt="cdk-esbuild">

*CDK constructs for [esbuild](https://github.com/evanw/esbuild), an extremely fast JavaScript bundler*

[Getting started](#getting-started) |
[Documentation](#documentation) | [API Reference](#api-reference) | [Python, .NET, & Go](#python-net-go) | [FAQ](#faq)

[![View on Construct Hub](https://constructs.dev/badge?package=%40mrgrain%2Fcdk-esbuild)](https://constructs.dev/packages/@mrgrain/cdk-esbuild)

## Why?

*esbuild* is an extremely fast bundler and minifier for TypeScript and JavaScript.
This package makes *esbuild* available to deploy AWS Lambda Functions, static websites or publish assets for further usage.

AWS CDK [supports *esbuild* for AWS Lambda Functions](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-lambda-nodejs-readme.html), but the implementation cannot be used with other Constructs and doesn't expose all of *esbuild*'s API.

## Getting started

Install `cdk-esbuild` for Node.js using your favorite package manager:

```sh
# npm
npm install @mrgrain/cdk-esbuild@4
# Yarn
yarn add @mrgrain/cdk-esbuild@4
# pnpm
pnpm add @mrgrain/cdk-esbuild@4
```

For Python, .NET or Go, use these commands:

```sh
# Python
pip install mrgrain.cdk-esbuild

# .NET
dotnet add package Mrgrain.CdkEsbuild

# Go
go get github.com/mrgrain/cdk-esbuild-go/cdkesbuild/v4
```

### AWS Lambda: Serverless function

> 💡 See [Lambda (TypeScript)](examples/typescript/lambda) and [Lambda (Python)](examples/typescript/lambda) for complete working examples of a how to deploy an AWS Lambda Function.

Use `TypeScriptCode` as the `code` of a [lambda function](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.Function.html#code):

```python
# Example automatically generated from non-compiling source. May contain errors.
bundled_code = TypeScriptCode("src/handler.ts")

fn = lambda_.Function(stack, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_18_X,
    handler="index.handler",
    code=bundled_code
)
```

### AWS S3: Static Website

> 💡 See [React App (TypeScript)](examples/typescript/website) for a complete working example of a how to deploy a React app to S3.

Use `TypeScriptSource` as one of the `sources` of a [static website deployment](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-deployment-readme.html#roadmap):

```python
website_bundle = TypeScriptSource("src/index.tsx")

website_bucket = s3.Bucket(stack, "WebsiteBucket",
    auto_delete_objects=True,
    public_read_access=True,
    removal_policy=cdk.RemovalPolicy.DESTROY,
    website_index_document="index.html"
)

s3deploy.BucketDeployment(stack, "DeployWebsite",
    destination_bucket=website_bucket,
    sources=[website_bundle]
)
```

### Amazon CloudWatch Synthetics: Canary monitoring

> 💡 See [Monitored Website (TypeScript)](examples/typescript/website) for a complete working example of a deployed and monitored website.

Synthetics runs a canary to produce traffic to an application for monitoring purposes. Use `TypeScriptCode` as the `code` of a Canary test:

> ℹ️ This feature depends on `@aws-cdk/aws-synthetics-alpha` which is in developer preview.
> Please install the package using the respective tool of your language.
> You may need to update your source code when upgrading to a newer version of this alpha package.

```python
bundled_code = TypeScriptCode("src/canary.ts",
    build_options=BuildOptions(
        outdir="nodejs/node_modules"
    )
)

canary = synthetics.Canary(stack, "MyCanary",
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_2,
    test=synthetics.Test.custom(
        code=bundled_code,
        handler="index.handler"
    )
)
```

## Documentation

The package exports various different constructs for use with AWS CDK features. The guiding design principal for this package is *"extend, don't replace"*. Expect constructs that you can provide as props, not complete replacements.

For use in **Lambda Functions** and **Synthetic Canaries**, the following classes implement `lambda.Code` ([reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.Code.html)) and `synthetics.Code` ([reference](https://docs.aws.amazon.com/cdk/api/v2/docs/@aws-cdk_aws-synthetics-alpha.Code.html)):

* `TypeScriptCode` & `JavaScriptCode`

Inline code is only supported by **Lambda**:

* `InlineTypeScriptCode` & `InlineJavaScriptCode`

For use with **S3 bucket deployments**, classes implementing `s3deploy.ISource` ([reference](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-deployment-readme.html)):

* `TypeScriptSource` & `JavaScriptSource`

> *Code and Source constructs seamlessly plug-in to other high-level CDK constructs. They share the same set of parameters, props and build options.*

The following classes power the other features. You normally won't have to use them, but they are there if you need them:

* `TypeScriptAsset` & `JavaScriptAsset` implements `s3.Asset` ([reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3_assets.Asset.html)) \
  creates an asset uploaded to S3 which can be referenced by other constructs
* `EsbuildBundler` implements `core.BundlingOptions` ([reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.BundlingOptions.html)) \
  provides an interface for a *esbuild* bundler wherever needed
* `EsbuildProvider` implements `IBuildProvider` and `ITransformProvider` \
  provides the default *esbuild* API implementation and can be replaced with a custom implementation

### [API Reference](API.md)

Auto-generated reference for Constructs, Classes and Structs.
This information is also available as part of your IDE's code completion.

### Python, .NET, Go

*Esbuild* requires a platform and architecture specific binary and currently has to be installed with a Node.js package manager like npm.

When using `cdk-esbuild` with Python, .NET or Go, the package will automatically detect local and global installations of the *esbuild* npm package.
If none can be found, it will fall back to dynamically installing a copy into a temporary location.
The exact algorithm of this mechanism must be treated as an implementation detail and should not be relied on.
It can however be configured to a certain extent.
See the examples below for more details.

This "best effort" approach makes it easy to get started.
But is not always desirable, for example in environments with limited network access or when guaranteed repeatability of builds is a concern.
You have several options to opt-out of this behavior.

#### Provide a controlled installation of *esbuild*

The first step is to install a version of *esbuild* that is controlled by you.

I **strongly recommend** to install *esbuild* as a local package.
The easiest approach is to manage an additional Node.js project at the root of your AWS CDK project.
*esbuild* can then be added to the `package.json` file and it is your responsibility to ensure required setup steps are taken in all environments like development machines and CI/CD systems.

Instead of installing the *esbuild* package in a local project, it can also be **installed globally** with `npm install -g esbuild` or a similar command.
This approach might be preferred if a build container is prepared ahead of time, thus avoiding repeated package installation.

#### Change the automatic package detection

The second step is to make `cdk-esbuild` aware of your chosen install location.
This step is optional, but it's a good idea to have the location or at least the method explicitly defined.

To do this, you can set the `esbuildModulePath` prop on a `EsbuildProvider`.
Either pass a known, absolute or relative path as value, or use the `EsbuildSource` helper to set the detection method.
Please refer to the [`EsbuildSource`](API.md#esbuildsource) reference for a complete list of available methods.

```python
# Use the standard Node.js algorithm to detect a locally installed package
EsbuildProvider(
    esbuild_module_path=EsbuildSource.node_js()
)

# Provide an explicit path
EsbuildProvider(
    esbuild_module_path="/home/user/node_modules/esbuild/lib/main.js"
)
```

As a no-code approach, the `CDK_ESBUILD_MODULE_PATH` environment variable can be set in the same way.
An advantage of this is that the path can easily be changed for different systems.
Setting the env variable can be used with any installation approach, but is typically paired with a global installation of the *esbuild* package.
Note that `esbuildModulePath` takes precedence.

#### Override the default detection method

For an AWS CDK app with many instances of `TypeScriptCode` etc. it would be annoying to change the above for every single one of them.
Luckily, the default can be changed for all usages per app:

```python
custom_module = EsbuildProvider(
    esbuild_module_path=EsbuildSource.global_paths()
)
EsbuildProvider.override_default_provider(custom_module)
```

### Customizing the Esbuild API

This package uses the *esbuild* JavaScript API.
In most situations the default API configuration will be suitable.
But sometimes it is required to configure *esbuild* differently or even provide a custom implementation.
Common reasons for this are:

* Using a pre-installed version of *esbuild* with Python, .NET or Go
* If features not supported by the synchronous API are required, e.g. support for plugins
* If the default version constraints for *esbuild* are not suitable
* To use a version of esbuild that is installed by any other means than `npm`, including Docker

For these scenarios, this package offers customization options and an interface to provide a custom implementation:

```python
# my_custom_build_provider: IBuildProvider

# my_custom_transform_provider: ITransformProvider


TypeScriptCode("src/handler.ts",
    build_provider=my_custom_build_provider
)

InlineTypeScriptCode("let x: number = 1",
    transform_provider=my_custom_transform_provider
)
```

#### Esbuild binary path

It is possible to override the binary used by *esbuild* by setting a property on `EsbuildProvider`.
This is the same as setting the `ESBUILD_BINARY_PATH` environment variable.
Defining the `esbuildBinaryPath` prop takes precedence.

```python
build_provider = EsbuildProvider(
    esbuild_binary_path="path/to/esbuild/binary"
)

# This will use a different esbuild binary
TypeScriptCode("src/handler.ts", build_provider=build_provider)
```

#### Esbuild module path

The Node.js module discovery algorithm will normally be used to find the *esbuild* package.
It can be useful to use specify a different module path, for example if a globally installed package should be used instead of a local version.

```python
build_provider = EsbuildProvider(
    esbuild_module_path="/home/user/node_modules/esbuild/lib/main.js"
)

# This will use a different esbuild module
TypeScriptCode("src/handler.ts", build_provider=build_provider)
```

Alternatively supported by setting the `CDK_ESBUILD_MODULE_PATH` environment variable, which will apply to all uses.
Defining the `esbuildModulePath` prop takes precedence.

If you are a Python, .NET or Go user, refer to the language specific guide for a more detailed explanation of this feature.

#### Custom Build and Transform API implementations

> 💡 See [esbuild plugins w/ TypeScript](examples/typescript/esbuild-with-plugins) for a complete working example of a custom Build API implementation.

A custom implementation can be provided by implementing `IBuildProvider` or `ITransformProvider`:

```python
@jsii.implements(IBuildProvider)
@jsii.implements(ITransformProvider)
class CustomEsbuild:
    def build_sync(self, *, bundle=None, splitting=None, preserveSymlinks=None, outfile=None, metafile=None, outdir=None, outbase=None, external=None, packages=None, alias=None, loader=None, resolveExtensions=None, mainFields=None, conditions=None, write=None, allowOverwrite=None, tsconfig=None, outExtension=None, publicPath=None, entryNames=None, chunkNames=None, assetNames=None, inject=None, banner=None, footer=None, absWorkingDir=None, nodePaths=None, sourcemap=None, legalComments=None, sourceRoot=None, sourcesContent=None, format=None, globalName=None, target=None, supported=None, platform=None, mangleProps=None, reserveProps=None, mangleQuoted=None, mangleCache=None, drop=None, minify=None, minifyWhitespace=None, minifyIdentifiers=None, minifySyntax=None, charset=None, treeShaking=None, ignoreAnnotations=None, jsx=None, jsxFactory=None, jsxFragment=None, jsxImportSource=None, jsxDev=None, jsxSideEffects=None, define=None, pure=None, keepNames=None, color=None, logLevel=None, logLimit=None, logOverride=None):
        pass

    def transform_sync(self, code, *, tsconfigRaw=None, sourcefile=None, loader=None, banner=None, footer=None, sourcemap=None, legalComments=None, sourceRoot=None, sourcesContent=None, format=None, globalName=None, target=None, supported=None, platform=None, mangleProps=None, reserveProps=None, mangleQuoted=None, mangleCache=None, drop=None, minify=None, minifyWhitespace=None, minifyIdentifiers=None, minifySyntax=None, charset=None, treeShaking=None, ignoreAnnotations=None, jsx=None, jsxFactory=None, jsxFragment=None, jsxImportSource=None, jsxDev=None, jsxSideEffects=None, define=None, pure=None, keepNames=None, color=None, logLevel=None, logLimit=None, logOverride=None):
        # custom implementation goes here, return transformed code
        return "transformed code"

# These will use the custom implementation
TypeScriptCode("src/handler.ts",
    build_provider=CustomEsbuild()
)
InlineTypeScriptCode("let x: number = 1",
    transform_provider=CustomEsbuild()
)
```

Instead of *esbuild*, the custom methods will be invoked with all computed options.
Custom implementations can amend, change or discard any of the options.

The `IBuildProvider` integration with CDK relies on the `outdir`/`outfile` values and it's usually required to use them unchanged.

`ITransformProvider` must return the transformed code as a string.

Failures and warnings should be printed to stderr and thrown as the respective *esbuild* error.

#### Overriding the default implementation providers

The default implementation can also be set for all usages of `TypeScriptCode` etc. in an AWS CDK app.
You can change the default for both APIs at once or set a different implementation for each of them.

```python
my_custom_esbuild_provider = MyCustomEsbuildProvider()

EsbuildProvider.override_default_provider(my_custom_esbuild_provider)
EsbuildProvider.override_default_build_provider(my_custom_esbuild_provider)
EsbuildProvider.override_default_transformation_provider(my_custom_esbuild_provider)

# This will use the custom provider without the need to define it as a prop
TypeScriptCode("src/handler.ts")
```

### Roadmap & Contributions

[The project's roadmap is available on GitHub.](https://github.com/users/mrgrain/projects/1/views/7)

Please submit feature requests as issues to the repository.
All contributions are welcome, no matter if they are for already planned or completely new features.

## FAQ

### Should I use this package in production?

This package is stable and ready to be used in production, as many do.
However *esbuild* has not yet released a version 1.0.0 and its API is still in active development.
Please read the guide on [esbuild's production readiness](https://esbuild.github.io/faq/#production-readiness).

Note that *esbuild* minor version upgrades are also introduced in **minor versions** of this package.
Since *esbuild* is pre v1, these versions typically introduce breaking changes and this package will inherit them.
To avoid this behavior, add the desired *esbuild* version as a dependency to your package.

### How do I upgrade from `cdk-esbuild` v3?

Please refer to the [v4 release notes](https://github.com/mrgrain/cdk-esbuild/releases/tag/v4.0.0) for a list of backwards incompatible changes and respective upgrade instructions.

### [TS/JS] Why am I getting the error `Cannot find module 'esbuild'`?

This package depends on *esbuild* as an optional dependencies. If optional dependencies are not installed automatically on your system (e.g. when using npm v4-6), install *esbuild* explicitly:

```console
npm install esbuild
```

### [TS/JS] How can I use a different version of *esbuild*?

Use the [override](https://docs.npmjs.com/cli/v9/configuring-npm/package-json?v=true#overrides) instructions for your package manager to force a specific version, for example:

```json
{
  "overrides": {
    "esbuild": "0.14.7"
  }
}
```

Build and Transform interfaces are relatively stable across *esbuild* versions.
However if any incompatibilities occur, `buildOptions` / `transformOptions` can be cast to `any`:

```python
bundled_code = TypeScriptCode("src/handler.ts",
    build_options={
        "unsupported_option": "value"
    }
)
```

### [Python/.NET/Go] How can I use a different version of *esbuild*?

Install the desired version of *esbuild* locally or globally [as described in the documentation above](#python-net-go).

Build and Transform interfaces are relatively stable across *esbuild* versions.
However if any incompatibilities occur, use the appropriate language features to cast any incompatible `buildOptions` / `transformOptions` to the correct types.

### Can I use this package in my published AWS CDK Construct?

It is possible to use `cdk-esbuild` in a published AWS CDK Construct library, but not recommended.
Always prefer to ship a compiled `.js` file or even bundle a zip archive in your package.
For AWS Lambda Functions, [projen provides an excellent solution](https://projen.io/awscdk.html#aws-lambda-functions).

If you do end up consuming `cdk-esbuild`, you will have to set `buildOptions.absWorkingDir`. The easiest way to do this, is to resolve the path based on the directory name of the calling file:

```js
// file: node_modules/construct-library/src/index.ts
const props = {
  buildOptions: {
    absWorkingDir: path.resolve(__dirname, ".."),
    // now: /user/local-app/node_modules/construct-library
  },
};
```

This will dynamically resolve to the correct path, wherever the package is installed. Please open an issue if you encounter any difficulties.

### Can I use this package with AWS CDK v1?

Yes, the `2.x.x` line of `cdk-esbuild` is compatible with AWS CDK v1. You can find the [documentation for it on the v2 branch](https://github.com/mrgrain/cdk-esbuild/tree/v2).

However, in line with AWS CDK v2, this version release now only receives security updates and critical bug fixes and support will fully end on June 1, 2023.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import aws_cdk.aws_s3_deployment as _aws_cdk_aws_s3_deployment_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.BuildOptions",
    jsii_struct_bases=[],
    name_mapping={
        "abs_working_dir": "absWorkingDir",
        "alias": "alias",
        "allow_overwrite": "allowOverwrite",
        "asset_names": "assetNames",
        "banner": "banner",
        "bundle": "bundle",
        "charset": "charset",
        "chunk_names": "chunkNames",
        "color": "color",
        "conditions": "conditions",
        "define": "define",
        "drop": "drop",
        "entry_names": "entryNames",
        "external": "external",
        "footer": "footer",
        "format": "format",
        "global_name": "globalName",
        "ignore_annotations": "ignoreAnnotations",
        "inject": "inject",
        "jsx": "jsx",
        "jsx_dev": "jsxDev",
        "jsx_factory": "jsxFactory",
        "jsx_fragment": "jsxFragment",
        "jsx_import_source": "jsxImportSource",
        "jsx_side_effects": "jsxSideEffects",
        "keep_names": "keepNames",
        "legal_comments": "legalComments",
        "loader": "loader",
        "log_level": "logLevel",
        "log_limit": "logLimit",
        "log_override": "logOverride",
        "main_fields": "mainFields",
        "mangle_cache": "mangleCache",
        "mangle_props": "mangleProps",
        "mangle_quoted": "mangleQuoted",
        "metafile": "metafile",
        "minify": "minify",
        "minify_identifiers": "minifyIdentifiers",
        "minify_syntax": "minifySyntax",
        "minify_whitespace": "minifyWhitespace",
        "node_paths": "nodePaths",
        "outbase": "outbase",
        "outdir": "outdir",
        "out_extension": "outExtension",
        "outfile": "outfile",
        "packages": "packages",
        "platform": "platform",
        "preserve_symlinks": "preserveSymlinks",
        "public_path": "publicPath",
        "pure": "pure",
        "reserve_props": "reserveProps",
        "resolve_extensions": "resolveExtensions",
        "sourcemap": "sourcemap",
        "source_root": "sourceRoot",
        "sources_content": "sourcesContent",
        "splitting": "splitting",
        "supported": "supported",
        "target": "target",
        "tree_shaking": "treeShaking",
        "tsconfig": "tsconfig",
        "write": "write",
    },
)
class BuildOptions:
    def __init__(
        self,
        *,
        abs_working_dir: typing.Optional[builtins.str] = None,
        alias: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allow_overwrite: typing.Optional[builtins.bool] = None,
        asset_names: typing.Optional[builtins.str] = None,
        banner: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bundle: typing.Optional[builtins.bool] = None,
        charset: typing.Optional[builtins.str] = None,
        chunk_names: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        entry_names: typing.Optional[builtins.str] = None,
        external: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        inject: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        metafile: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        node_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbase: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        out_extension: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outfile: typing.Optional[builtins.str] = None,
        packages: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        preserve_symlinks: typing.Optional[builtins.bool] = None,
        public_path: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        resolve_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        splitting: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig: typing.Optional[builtins.str] = None,
        write: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param abs_working_dir: Documentation: https://esbuild.github.io/api/#working-directory.
        :param alias: Documentation: https://esbuild.github.io/api/#alias.
        :param allow_overwrite: Documentation: https://esbuild.github.io/api/#allow-overwrite.
        :param asset_names: Documentation: https://esbuild.github.io/api/#asset-names.
        :param banner: Documentation: https://esbuild.github.io/api/#banner.
        :param bundle: Documentation: https://esbuild.github.io/api/#bundle.
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param chunk_names: Documentation: https://esbuild.github.io/api/#chunk-names.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param conditions: Documentation: https://esbuild.github.io/api/#conditions.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param entry_names: Documentation: https://esbuild.github.io/api/#entry-names.
        :param external: Documentation: https://esbuild.github.io/api/#external.
        :param footer: Documentation: https://esbuild.github.io/api/#footer.
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param inject: Documentation: https://esbuild.github.io/api/#inject.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: Documentation: https://esbuild.github.io/api/#loader.
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param main_fields: Documentation: https://esbuild.github.io/api/#main-fields.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param metafile: Documentation: https://esbuild.github.io/api/#metafile.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param node_paths: Documentation: https://esbuild.github.io/api/#node-paths.
        :param outbase: Documentation: https://esbuild.github.io/api/#outbase.
        :param outdir: Documentation: https://esbuild.github.io/api/#outdir.
        :param out_extension: Documentation: https://esbuild.github.io/api/#out-extension.
        :param outfile: Documentation: https://esbuild.github.io/api/#outfile.
        :param packages: Documentation: https://esbuild.github.io/api/#packages.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param preserve_symlinks: Documentation: https://esbuild.github.io/api/#preserve-symlinks.
        :param public_path: Documentation: https://esbuild.github.io/api/#public-path.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param resolve_extensions: Documentation: https://esbuild.github.io/api/#resolve-extensions.
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param splitting: Documentation: https://esbuild.github.io/api/#splitting.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig: Documentation: https://esbuild.github.io/api/#tsconfig.
        :param write: Documentation: https://esbuild.github.io/api/#write.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3dbfe8b02ff3b7a13b707799738cc16cd402c4e3086f60eb8f86814c6b2680)
            check_type(argname="argument abs_working_dir", value=abs_working_dir, expected_type=type_hints["abs_working_dir"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_overwrite", value=allow_overwrite, expected_type=type_hints["allow_overwrite"])
            check_type(argname="argument asset_names", value=asset_names, expected_type=type_hints["asset_names"])
            check_type(argname="argument banner", value=banner, expected_type=type_hints["banner"])
            check_type(argname="argument bundle", value=bundle, expected_type=type_hints["bundle"])
            check_type(argname="argument charset", value=charset, expected_type=type_hints["charset"])
            check_type(argname="argument chunk_names", value=chunk_names, expected_type=type_hints["chunk_names"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument define", value=define, expected_type=type_hints["define"])
            check_type(argname="argument drop", value=drop, expected_type=type_hints["drop"])
            check_type(argname="argument entry_names", value=entry_names, expected_type=type_hints["entry_names"])
            check_type(argname="argument external", value=external, expected_type=type_hints["external"])
            check_type(argname="argument footer", value=footer, expected_type=type_hints["footer"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument global_name", value=global_name, expected_type=type_hints["global_name"])
            check_type(argname="argument ignore_annotations", value=ignore_annotations, expected_type=type_hints["ignore_annotations"])
            check_type(argname="argument inject", value=inject, expected_type=type_hints["inject"])
            check_type(argname="argument jsx", value=jsx, expected_type=type_hints["jsx"])
            check_type(argname="argument jsx_dev", value=jsx_dev, expected_type=type_hints["jsx_dev"])
            check_type(argname="argument jsx_factory", value=jsx_factory, expected_type=type_hints["jsx_factory"])
            check_type(argname="argument jsx_fragment", value=jsx_fragment, expected_type=type_hints["jsx_fragment"])
            check_type(argname="argument jsx_import_source", value=jsx_import_source, expected_type=type_hints["jsx_import_source"])
            check_type(argname="argument jsx_side_effects", value=jsx_side_effects, expected_type=type_hints["jsx_side_effects"])
            check_type(argname="argument keep_names", value=keep_names, expected_type=type_hints["keep_names"])
            check_type(argname="argument legal_comments", value=legal_comments, expected_type=type_hints["legal_comments"])
            check_type(argname="argument loader", value=loader, expected_type=type_hints["loader"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument log_limit", value=log_limit, expected_type=type_hints["log_limit"])
            check_type(argname="argument log_override", value=log_override, expected_type=type_hints["log_override"])
            check_type(argname="argument main_fields", value=main_fields, expected_type=type_hints["main_fields"])
            check_type(argname="argument mangle_cache", value=mangle_cache, expected_type=type_hints["mangle_cache"])
            check_type(argname="argument mangle_props", value=mangle_props, expected_type=type_hints["mangle_props"])
            check_type(argname="argument mangle_quoted", value=mangle_quoted, expected_type=type_hints["mangle_quoted"])
            check_type(argname="argument metafile", value=metafile, expected_type=type_hints["metafile"])
            check_type(argname="argument minify", value=minify, expected_type=type_hints["minify"])
            check_type(argname="argument minify_identifiers", value=minify_identifiers, expected_type=type_hints["minify_identifiers"])
            check_type(argname="argument minify_syntax", value=minify_syntax, expected_type=type_hints["minify_syntax"])
            check_type(argname="argument minify_whitespace", value=minify_whitespace, expected_type=type_hints["minify_whitespace"])
            check_type(argname="argument node_paths", value=node_paths, expected_type=type_hints["node_paths"])
            check_type(argname="argument outbase", value=outbase, expected_type=type_hints["outbase"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument out_extension", value=out_extension, expected_type=type_hints["out_extension"])
            check_type(argname="argument outfile", value=outfile, expected_type=type_hints["outfile"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument preserve_symlinks", value=preserve_symlinks, expected_type=type_hints["preserve_symlinks"])
            check_type(argname="argument public_path", value=public_path, expected_type=type_hints["public_path"])
            check_type(argname="argument pure", value=pure, expected_type=type_hints["pure"])
            check_type(argname="argument reserve_props", value=reserve_props, expected_type=type_hints["reserve_props"])
            check_type(argname="argument resolve_extensions", value=resolve_extensions, expected_type=type_hints["resolve_extensions"])
            check_type(argname="argument sourcemap", value=sourcemap, expected_type=type_hints["sourcemap"])
            check_type(argname="argument source_root", value=source_root, expected_type=type_hints["source_root"])
            check_type(argname="argument sources_content", value=sources_content, expected_type=type_hints["sources_content"])
            check_type(argname="argument splitting", value=splitting, expected_type=type_hints["splitting"])
            check_type(argname="argument supported", value=supported, expected_type=type_hints["supported"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument tree_shaking", value=tree_shaking, expected_type=type_hints["tree_shaking"])
            check_type(argname="argument tsconfig", value=tsconfig, expected_type=type_hints["tsconfig"])
            check_type(argname="argument write", value=write, expected_type=type_hints["write"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if abs_working_dir is not None:
            self._values["abs_working_dir"] = abs_working_dir
        if alias is not None:
            self._values["alias"] = alias
        if allow_overwrite is not None:
            self._values["allow_overwrite"] = allow_overwrite
        if asset_names is not None:
            self._values["asset_names"] = asset_names
        if banner is not None:
            self._values["banner"] = banner
        if bundle is not None:
            self._values["bundle"] = bundle
        if charset is not None:
            self._values["charset"] = charset
        if chunk_names is not None:
            self._values["chunk_names"] = chunk_names
        if color is not None:
            self._values["color"] = color
        if conditions is not None:
            self._values["conditions"] = conditions
        if define is not None:
            self._values["define"] = define
        if drop is not None:
            self._values["drop"] = drop
        if entry_names is not None:
            self._values["entry_names"] = entry_names
        if external is not None:
            self._values["external"] = external
        if footer is not None:
            self._values["footer"] = footer
        if format is not None:
            self._values["format"] = format
        if global_name is not None:
            self._values["global_name"] = global_name
        if ignore_annotations is not None:
            self._values["ignore_annotations"] = ignore_annotations
        if inject is not None:
            self._values["inject"] = inject
        if jsx is not None:
            self._values["jsx"] = jsx
        if jsx_dev is not None:
            self._values["jsx_dev"] = jsx_dev
        if jsx_factory is not None:
            self._values["jsx_factory"] = jsx_factory
        if jsx_fragment is not None:
            self._values["jsx_fragment"] = jsx_fragment
        if jsx_import_source is not None:
            self._values["jsx_import_source"] = jsx_import_source
        if jsx_side_effects is not None:
            self._values["jsx_side_effects"] = jsx_side_effects
        if keep_names is not None:
            self._values["keep_names"] = keep_names
        if legal_comments is not None:
            self._values["legal_comments"] = legal_comments
        if loader is not None:
            self._values["loader"] = loader
        if log_level is not None:
            self._values["log_level"] = log_level
        if log_limit is not None:
            self._values["log_limit"] = log_limit
        if log_override is not None:
            self._values["log_override"] = log_override
        if main_fields is not None:
            self._values["main_fields"] = main_fields
        if mangle_cache is not None:
            self._values["mangle_cache"] = mangle_cache
        if mangle_props is not None:
            self._values["mangle_props"] = mangle_props
        if mangle_quoted is not None:
            self._values["mangle_quoted"] = mangle_quoted
        if metafile is not None:
            self._values["metafile"] = metafile
        if minify is not None:
            self._values["minify"] = minify
        if minify_identifiers is not None:
            self._values["minify_identifiers"] = minify_identifiers
        if minify_syntax is not None:
            self._values["minify_syntax"] = minify_syntax
        if minify_whitespace is not None:
            self._values["minify_whitespace"] = minify_whitespace
        if node_paths is not None:
            self._values["node_paths"] = node_paths
        if outbase is not None:
            self._values["outbase"] = outbase
        if outdir is not None:
            self._values["outdir"] = outdir
        if out_extension is not None:
            self._values["out_extension"] = out_extension
        if outfile is not None:
            self._values["outfile"] = outfile
        if packages is not None:
            self._values["packages"] = packages
        if platform is not None:
            self._values["platform"] = platform
        if preserve_symlinks is not None:
            self._values["preserve_symlinks"] = preserve_symlinks
        if public_path is not None:
            self._values["public_path"] = public_path
        if pure is not None:
            self._values["pure"] = pure
        if reserve_props is not None:
            self._values["reserve_props"] = reserve_props
        if resolve_extensions is not None:
            self._values["resolve_extensions"] = resolve_extensions
        if sourcemap is not None:
            self._values["sourcemap"] = sourcemap
        if source_root is not None:
            self._values["source_root"] = source_root
        if sources_content is not None:
            self._values["sources_content"] = sources_content
        if splitting is not None:
            self._values["splitting"] = splitting
        if supported is not None:
            self._values["supported"] = supported
        if target is not None:
            self._values["target"] = target
        if tree_shaking is not None:
            self._values["tree_shaking"] = tree_shaking
        if tsconfig is not None:
            self._values["tsconfig"] = tsconfig
        if write is not None:
            self._values["write"] = write

    @builtins.property
    def abs_working_dir(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#working-directory.'''
        result = self._values.get("abs_working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#alias.'''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def allow_overwrite(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#allow-overwrite.'''
        result = self._values.get("allow_overwrite")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def asset_names(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#asset-names.'''
        result = self._values.get("asset_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def banner(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#banner.'''
        result = self._values.get("banner")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bundle(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#bundle.'''
        result = self._values.get("bundle")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def charset(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#charset.'''
        result = self._values.get("charset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chunk_names(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#chunk-names.'''
        result = self._values.get("chunk_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#color.'''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#conditions.'''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def define(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#define.'''
        result = self._values.get("define")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def drop(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#drop.'''
        result = self._values.get("drop")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entry_names(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#entry-names.'''
        result = self._values.get("entry_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#external.'''
        result = self._values.get("external")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def footer(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#footer.'''
        result = self._values.get("footer")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#format.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_name(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#global-name.'''
        result = self._values.get("global_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_annotations(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#ignore-annotations.'''
        result = self._values.get("ignore_annotations")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def inject(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#inject.'''
        result = self._values.get("inject")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jsx(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx.'''
        result = self._values.get("jsx")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_dev(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-development.'''
        result = self._values.get("jsx_dev")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx_factory(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-factory.'''
        result = self._values.get("jsx_factory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_fragment(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-fragment.'''
        result = self._values.get("jsx_fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_import_source(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-import-source.'''
        result = self._values.get("jsx_import_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_side_effects(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-side-effects.'''
        result = self._values.get("jsx_side_effects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def keep_names(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#keep-names.'''
        result = self._values.get("keep_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def legal_comments(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#legal-comments.'''
        result = self._values.get("legal_comments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def loader(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#loader.'''
        result = self._values.get("loader")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#log-level.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_limit(self) -> typing.Optional[jsii.Number]:
        '''Documentation: https://esbuild.github.io/api/#log-limit.'''
        result = self._values.get("log_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_override(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#log-override.'''
        result = self._values.get("log_override")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def main_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#main-fields.'''
        result = self._values.get("main_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mangle_cache(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_cache")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]], result)

    @builtins.property
    def mangle_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def mangle_quoted(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_quoted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metafile(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#metafile.'''
        result = self._values.get("metafile")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_identifiers(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_identifiers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_syntax(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_syntax")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_whitespace(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_whitespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#node-paths.'''
        result = self._values.get("node_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outbase(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#outbase.'''
        result = self._values.get("outbase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#outdir.'''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def out_extension(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#out-extension.'''
        result = self._values.get("out_extension")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def outfile(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#outfile.'''
        result = self._values.get("outfile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#packages.'''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#platform.'''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_symlinks(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#preserve-symlinks.'''
        result = self._values.get("preserve_symlinks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def public_path(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#public-path.'''
        result = self._values.get("public_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pure(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#pure.'''
        result = self._values.get("pure")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reserve_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("reserve_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resolve_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#resolve-extensions.'''
        result = self._values.get("resolve_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sourcemap(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#sourcemap.'''
        result = self._values.get("sourcemap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], result)

    @builtins.property
    def source_root(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#source-root.'''
        result = self._values.get("source_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources_content(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#sources-content.'''
        result = self._values.get("sources_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def splitting(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#splitting.'''
        result = self._values.get("splitting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supported(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.bool]]:
        '''Documentation: https://esbuild.github.io/api/#supported.'''
        result = self._values.get("supported")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.bool]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''Documentation: https://esbuild.github.io/api/#target.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def tree_shaking(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#tree-shaking.'''
        result = self._values.get("tree_shaking")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tsconfig(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#tsconfig.'''
        result = self._values.get("tsconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def write(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#write.'''
        result = self._values.get("write")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.BundlerProps",
    jsii_struct_bases=[],
    name_mapping={
        "build_options": "buildOptions",
        "build_provider": "buildProvider",
        "copy_dir": "copyDir",
    },
)
class BundlerProps:
    def __init__(
        self,
        *,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional["IBuildProvider"] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if isinstance(build_options, dict):
            build_options = BuildOptions(**build_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9873d08db3203496e0d96907173153080076971ae0098d003ebff0ccaffdb97)
            check_type(argname="argument build_options", value=build_options, expected_type=type_hints["build_options"])
            check_type(argname="argument build_provider", value=build_provider, expected_type=type_hints["build_provider"])
            check_type(argname="argument copy_dir", value=copy_dir, expected_type=type_hints["copy_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_options is not None:
            self._values["build_options"] = build_options
        if build_provider is not None:
            self._values["build_provider"] = build_provider
        if copy_dir is not None:
            self._values["copy_dir"] = copy_dir

    @builtins.property
    def build_options(self) -> typing.Optional[BuildOptions]:
        '''Build options passed on to esbuild. Please refer to the esbuild Build API docs for details.

        - ``buildOptions.outdir: string``
          The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory.
          For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory.
          *Cannot be used together with ``outfile``*.
        - ``buildOptions.outfile: string``
          Relative path to a file inside the CDK asset output directory.
          For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point.
          *Cannot be used with multiple entryPoints or together with ``outdir``.*
        - ``buildOptions.absWorkingDir: string``
          Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_.
          If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).

        :see: https://esbuild.github.io/api/#build-api
        '''
        result = self._values.get("build_options")
        return typing.cast(typing.Optional[BuildOptions], result)

    @builtins.property
    def build_provider(self) -> typing.Optional["IBuildProvider"]:
        '''The esbuild Build API implementation to be used.

        Configure the default ``EsbuildProvider`` for more options or
        provide a custom ``IBuildProvider`` as an escape hatch.

        :default: new EsbuildProvider()
        '''
        result = self._values.get("build_provider")
        return typing.cast(typing.Optional["IBuildProvider"], result)

    @builtins.property
    def copy_dir(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]]:
        '''Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs.

        - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory.
        - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied.

        Therefore the following values for ``copyDir`` are all equivalent::

           { copyDir: "path/to/source" }
           { copyDir: ["path/to/source"] }
           { copyDir: { ".": "path/to/source" } }
           { copyDir: { ".": ["path/to/source"] } }

        The destination cannot be outside of the asset staging directory.
        If you are receiving the error "Cannot copy files to outside of the asset staging directory."
        you are likely using ``..`` or an absolute path as key on the ``copyDir`` map.
        Instead use only relative paths and avoid ``..``.
        '''
        result = self._values.get("copy_dir")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.CodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "inline_code": "inlineCode",
        "s3_location": "s3Location",
    },
)
class CodeConfig:
    def __init__(
        self,
        *,
        image: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.CodeImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        inline_code: typing.Optional[builtins.str] = None,
        s3_location: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.Location, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Result of binding ``Code`` into a ``Function``.

        :param image: Docker image configuration (mutually exclusive with ``s3Location`` and ``inlineCode``). Default: - code is not an ECR container image
        :param inline_code: Inline code (mutually exclusive with ``s3Location`` and ``image``). Default: - code is not inline code
        :param s3_location: The location of the code in S3 (mutually exclusive with ``inlineCode`` and ``image``). Default: - code is not an s3 location
        '''
        if isinstance(image, dict):
            image = _aws_cdk_aws_lambda_ceddda9d.CodeImageConfig(**image)
        if isinstance(s3_location, dict):
            s3_location = _aws_cdk_aws_s3_ceddda9d.Location(**s3_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c185489c0b0ad068a8687186a8aaa4be606d632824af7246f2c55827feaacf)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument inline_code", value=inline_code, expected_type=type_hints["inline_code"])
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image is not None:
            self._values["image"] = image
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if s3_location is not None:
            self._values["s3_location"] = s3_location

    @builtins.property
    def image(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.CodeImageConfig]:
        '''Docker image configuration (mutually exclusive with ``s3Location`` and ``inlineCode``).

        :default: - code is not an ECR container image
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.CodeImageConfig], result)

    @builtins.property
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''Inline code (mutually exclusive with ``s3Location`` and ``image``).

        :default: - code is not inline code
        '''
        result = self._values.get("inline_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_location(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Location]:
        '''The location of the code in S3 (mutually exclusive with ``inlineCode`` and ``image``).

        :default: - code is not an s3 location
        '''
        result = self._values.get("s3_location")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Location], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.CompilerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "imports_not_used_as_values": "importsNotUsedAsValues",
        "jsx_factory": "jsxFactory",
        "jsx_fragment_factory": "jsxFragmentFactory",
        "preserve_value_imports": "preserveValueImports",
        "use_define_for_class_fields": "useDefineForClassFields",
    },
)
class CompilerOptions:
    def __init__(
        self,
        *,
        imports_not_used_as_values: typing.Optional[builtins.str] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment_factory: typing.Optional[builtins.str] = None,
        preserve_value_imports: typing.Optional[builtins.bool] = None,
        use_define_for_class_fields: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param imports_not_used_as_values: 
        :param jsx_factory: 
        :param jsx_fragment_factory: 
        :param preserve_value_imports: 
        :param use_define_for_class_fields: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b682d31bc71983a448565f5ef0a021abb3aeaf127a6dab66c921bef47f98592)
            check_type(argname="argument imports_not_used_as_values", value=imports_not_used_as_values, expected_type=type_hints["imports_not_used_as_values"])
            check_type(argname="argument jsx_factory", value=jsx_factory, expected_type=type_hints["jsx_factory"])
            check_type(argname="argument jsx_fragment_factory", value=jsx_fragment_factory, expected_type=type_hints["jsx_fragment_factory"])
            check_type(argname="argument preserve_value_imports", value=preserve_value_imports, expected_type=type_hints["preserve_value_imports"])
            check_type(argname="argument use_define_for_class_fields", value=use_define_for_class_fields, expected_type=type_hints["use_define_for_class_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if imports_not_used_as_values is not None:
            self._values["imports_not_used_as_values"] = imports_not_used_as_values
        if jsx_factory is not None:
            self._values["jsx_factory"] = jsx_factory
        if jsx_fragment_factory is not None:
            self._values["jsx_fragment_factory"] = jsx_fragment_factory
        if preserve_value_imports is not None:
            self._values["preserve_value_imports"] = preserve_value_imports
        if use_define_for_class_fields is not None:
            self._values["use_define_for_class_fields"] = use_define_for_class_fields

    @builtins.property
    def imports_not_used_as_values(self) -> typing.Optional[builtins.str]:
        result = self._values.get("imports_not_used_as_values")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_factory(self) -> typing.Optional[builtins.str]:
        result = self._values.get("jsx_factory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_fragment_factory(self) -> typing.Optional[builtins.str]:
        result = self._values.get("jsx_fragment_factory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_value_imports(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("preserve_value_imports")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_define_for_class_fields(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("use_define_for_class_fields")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompilerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EsbuildAsset(
    _aws_cdk_aws_s3_assets_ceddda9d.Asset,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.EsbuildAsset",
):
    '''(experimental) Represents a generic esbuild asset.

    You should always use ``TypeScriptAsset`` or ``JavaScriptAsset``.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        asset_hash: typing.Optional[builtins.str] = None,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional["IBuildProvider"] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ececb4940ec6eae1c73365c13ad8bd754b062cb59e54a4e520ed5b39927f70)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssetProps(
            entry_points=entry_points,
            asset_hash=asset_hash,
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class EsbuildBundler(
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.EsbuildBundler",
):
    '''(experimental) Low-level construct that can be used where ``BundlingOptions`` are required.

    This class directly interfaces with esbuild and provides almost no configuration safeguards.

    :stability: experimental
    '''

    def __init__(
        self,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        *,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional["IBuildProvider"] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param entry_points: (experimental) A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3093569ed2b9b16c3c9014d1d3b5429adba0bf4de17908bc72728a57bb554c84)
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
        props = BundlerProps(
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [entry_points, props])

    @builtins.property
    @jsii.member(jsii_name="entryPoints")
    def entry_points(
        self,
    ) -> typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A path or list or map of paths to the entry points of your code.

        Relative paths are by default resolved from the current working directory.
        To change the working directory, see ``buildOptions.absWorkingDir``.

        Absolute paths can be used if files are part of the working directory.

        Examples:

        - ``'src/index.ts'``
        - ``require.resolve('./lambda')``
        - ``['src/index.ts', 'src/util.ts']``
        - ``{one: 'src/two.ts', two: 'src/one.ts'}``

        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "entryPoints"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_ceddda9d.DockerImage:
        '''
        :deprecated: This value is ignored since the bundler is always using a locally installed version of esbuild. However the property is required to comply with the ``BundlingOptions`` interface.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_ceddda9d.DockerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(self) -> _aws_cdk_ceddda9d.ILocalBundling:
        '''(experimental) Implementation of ``ILocalBundling`` interface, responsible for calling esbuild functions.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.ILocalBundling, jsii.get(self, "local"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> BundlerProps:
        '''(experimental) Props to change the behavior of the bundler.

        :stability: experimental
        '''
        return typing.cast(BundlerProps, jsii.get(self, "props"))


class EsbuildCode(
    _aws_cdk_aws_lambda_ceddda9d.Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.EsbuildCode",
):
    '''(experimental) Represents a generic esbuild code bundle.

    You should always use ``TypeScriptCode`` or ``JavaScriptCode``.

    :stability: experimental
    '''

    def __init__(
        self,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        props: typing.Union[typing.Union["JavaScriptCodeProps", typing.Dict[builtins.str, typing.Any]], typing.Union["TypeScriptCodeProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param props: Props to change the behavior of the bundler. Default values for ``props.buildOptions``: - ``bundle=true`` - ``platform=node`` - ``target=nodeX`` with X being the major node version running locally

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240365991669493923be1f0bfe12c1cc48bb10fe4c8a3111ab380790be41ccdb)
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [entry_points, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_lambda_ceddda9d.CodeConfig:
        '''(experimental) Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b721a6ee79f34aa33e63b2e59198a8a9838b1b0a4f6f2dda376f64ac2fd3289)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.CodeConfig, jsii.invoke(self, "bind", [scope]))

    @jsii.member(jsii_name="bindToResource")
    def bind_to_resource(
        self,
        resource: _aws_cdk_ceddda9d.CfnResource,
        *,
        resource_property: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Called after the CFN function resource has been created to allow the code class to bind to it.

        Specifically it's required to allow assets to add
        metadata for tooling like SAM CLI to be able to find their origins.

        :param resource: -
        :param resource_property: The name of the CloudFormation property to annotate with asset metadata. Default: Code
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f91f1d460a1f2d5cc64a5396f606c04ca6addf6527dd68a11a6d06d10158a64)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        options = _aws_cdk_aws_lambda_ceddda9d.ResourceBindOptions(
            resource_property=resource_property
        )

        return typing.cast(None, jsii.invoke(self, "bindToResource", [resource, options]))

    @jsii.member(jsii_name="getAsset")
    def _get_asset(self, scope: _constructs_77d1e7e8.Construct) -> EsbuildAsset:
        '''
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37de67b53e05897576c1062e32e3fe6075755b5a74e738ef4d3be53583e2153a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(EsbuildAsset, jsii.invoke(self, "getAsset", [scope]))

    @builtins.property
    @jsii.member(jsii_name="entryPoints")
    def entry_points(
        self,
    ) -> typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]]:
        '''A path or list or map of paths to the entry points of your code.

        Relative paths are by default resolved from the current working directory.
        To change the working directory, see ``buildOptions.absWorkingDir``.

        Absolute paths can be used if files are part of the working directory.

        Examples:

        - ``'src/index.ts'``
        - ``require.resolve('./lambda')``
        - ``['src/index.ts', 'src/util.ts']``
        - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        '''
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "entryPoints"))

    @builtins.property
    @jsii.member(jsii_name="asset")
    def _asset(self) -> EsbuildAsset:
        '''
        :stability: experimental
        '''
        return typing.cast(EsbuildAsset, jsii.get(self, "asset"))

    @_asset.setter
    def _asset(self, value: EsbuildAsset) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d305fae366aedae68d382d67dcb5b325fddf4dd255defe51b88d29cf64ba09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asset", value)

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> builtins.bool:
        '''(deprecated) Determines whether this Code is inline code or not.

        :deprecated: this value is ignored since inline is now determined based on the the inlineCode field of CodeConfig returned from bind().

        :stability: deprecated
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isInline"))

    @is_inline.setter
    def is_inline(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1dae3d5ed0d2c7458d21f336873b06a83119c1d01c6e4efdf3f4f083d5fc0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isInline", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "AssetProps":
        '''
        :stability: experimental
        '''
        return typing.cast("AssetProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "AssetProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfd6f14403c8fe61b069ea91e6f7e824c9809aadbf0334c47d49474d2095e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.EsbuildProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "esbuild_binary_path": "esbuildBinaryPath",
        "esbuild_module_path": "esbuildModulePath",
    },
)
class EsbuildProviderProps:
    def __init__(
        self,
        *,
        esbuild_binary_path: typing.Optional[builtins.str] = None,
        esbuild_module_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configure the default EsbuildProvider.

        :param esbuild_binary_path: Path to the binary used by esbuild. This is the same as setting the ESBUILD_BINARY_PATH environment variable.
        :param esbuild_module_path: Absolute path to the esbuild module JS file. E.g. "/home/user/.npm/node_modules/esbuild/lib/main.js" If not set, the module path will be determined in the following order: - Use a path from the ``CDK_ESBUILD_MODULE_PATH`` environment variable - In TypeScript, fallback to the default Node.js package resolution mechanism - All other languages (Python, Go, .NET, Java) use an automatic "best effort" resolution mechanism. The exact algorithm of this mechanism is considered an implementation detail and should not be relied on. If ``esbuild`` cannot be found, it might be installed dynamically to a temporary location. To opt-out of this behavior, set either ``esbuildModulePath`` or ``CDK_ESBUILD_MODULE_PATH`` env variable. Use the static methods on ``EsbuildSource`` to customize the default behavior. Default: - ``CDK_ESBUILD_MODULE_PATH`` or package resolution (see description)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e2e8be5e24a7fca00969e5b068680339e16f35bbdb62130ad26ff1caaf8318)
            check_type(argname="argument esbuild_binary_path", value=esbuild_binary_path, expected_type=type_hints["esbuild_binary_path"])
            check_type(argname="argument esbuild_module_path", value=esbuild_module_path, expected_type=type_hints["esbuild_module_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if esbuild_binary_path is not None:
            self._values["esbuild_binary_path"] = esbuild_binary_path
        if esbuild_module_path is not None:
            self._values["esbuild_module_path"] = esbuild_module_path

    @builtins.property
    def esbuild_binary_path(self) -> typing.Optional[builtins.str]:
        '''Path to the binary used by esbuild.

        This is the same as setting the ESBUILD_BINARY_PATH environment variable.
        '''
        result = self._values.get("esbuild_binary_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def esbuild_module_path(self) -> typing.Optional[builtins.str]:
        '''Absolute path to the esbuild module JS file.

        E.g. "/home/user/.npm/node_modules/esbuild/lib/main.js"

        If not set, the module path will be determined in the following order:

        - Use a path from the ``CDK_ESBUILD_MODULE_PATH`` environment variable
        - In TypeScript, fallback to the default Node.js package resolution mechanism
        - All other languages (Python, Go, .NET, Java) use an automatic "best effort" resolution mechanism.
          The exact algorithm of this mechanism is considered an implementation detail and should not be relied on.
          If ``esbuild`` cannot be found, it might be installed dynamically to a temporary location.
          To opt-out of this behavior, set either ``esbuildModulePath`` or ``CDK_ESBUILD_MODULE_PATH`` env variable.

        Use the static methods on ``EsbuildSource`` to customize the default behavior.

        :default: - ``CDK_ESBUILD_MODULE_PATH`` or package resolution (see description)
        '''
        result = self._values.get("esbuild_module_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EsbuildProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EsbuildSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.EsbuildSource",
):
    @jsii.member(jsii_name="anywhere")
    @builtins.classmethod
    def anywhere(cls) -> typing.Optional[builtins.str]:
        '''Try to find the module in most common paths.'''
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "anywhere", []))

    @jsii.member(jsii_name="auto")
    @builtins.classmethod
    def auto(cls) -> builtins.str:
        '''First try to find to module, then install it to a temporary location.'''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "auto", []))

    @jsii.member(jsii_name="globalPaths")
    @builtins.classmethod
    def global_paths(cls) -> typing.Optional[builtins.str]:
        '''Try to find the module in common global installation paths.'''
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "globalPaths", []))

    @jsii.member(jsii_name="install")
    @builtins.classmethod
    def install(cls) -> builtins.str:
        '''Install the module to a temporary location.'''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "install", []))

    @jsii.member(jsii_name="nodeJs")
    @builtins.classmethod
    def node_js(cls) -> builtins.str:
        '''Require module by name, do not attempt to find it anywhere else.'''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "nodeJs", []))

    @jsii.member(jsii_name="platformDefault")
    @builtins.classmethod
    def platform_default(cls) -> builtins.str:
        '''``EsbuildSource.nodeJs()`` for NodeJs, ``EsbuildSource.auto()`` for all other languages.'''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "platformDefault", []))


@jsii.interface(jsii_type="@mrgrain/cdk-esbuild.IBuildProvider")
class IBuildProvider(typing_extensions.Protocol):
    '''Provides an implementation of the esbuild Build API.'''

    @jsii.member(jsii_name="buildSync")
    def build_sync(
        self,
        *,
        entry_points: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]]] = None,
        abs_working_dir: typing.Optional[builtins.str] = None,
        alias: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allow_overwrite: typing.Optional[builtins.bool] = None,
        asset_names: typing.Optional[builtins.str] = None,
        banner: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bundle: typing.Optional[builtins.bool] = None,
        charset: typing.Optional[builtins.str] = None,
        chunk_names: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        entry_names: typing.Optional[builtins.str] = None,
        external: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        inject: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        metafile: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        node_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbase: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        out_extension: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outfile: typing.Optional[builtins.str] = None,
        packages: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        preserve_symlinks: typing.Optional[builtins.bool] = None,
        public_path: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        resolve_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        splitting: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig: typing.Optional[builtins.str] = None,
        write: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''A method implementing the code build.

        During synth time, the method will receive all computed ``BuildOptions`` from the bundler.

        It MUST implement any output options to integrate correctly and MAY use any other options.
        On failure, it SHOULD print any warnings & errors to stderr and throw a ``BuildFailure`` to inform the bundler.

        :param entry_points: Documentation: https://esbuild.github.io/api/#entry-points.
        :param abs_working_dir: Documentation: https://esbuild.github.io/api/#working-directory.
        :param alias: Documentation: https://esbuild.github.io/api/#alias.
        :param allow_overwrite: Documentation: https://esbuild.github.io/api/#allow-overwrite.
        :param asset_names: Documentation: https://esbuild.github.io/api/#asset-names.
        :param banner: Documentation: https://esbuild.github.io/api/#banner.
        :param bundle: Documentation: https://esbuild.github.io/api/#bundle.
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param chunk_names: Documentation: https://esbuild.github.io/api/#chunk-names.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param conditions: Documentation: https://esbuild.github.io/api/#conditions.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param entry_names: Documentation: https://esbuild.github.io/api/#entry-names.
        :param external: Documentation: https://esbuild.github.io/api/#external.
        :param footer: Documentation: https://esbuild.github.io/api/#footer.
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param inject: Documentation: https://esbuild.github.io/api/#inject.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: Documentation: https://esbuild.github.io/api/#loader.
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param main_fields: Documentation: https://esbuild.github.io/api/#main-fields.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param metafile: Documentation: https://esbuild.github.io/api/#metafile.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param node_paths: Documentation: https://esbuild.github.io/api/#node-paths.
        :param outbase: Documentation: https://esbuild.github.io/api/#outbase.
        :param outdir: Documentation: https://esbuild.github.io/api/#outdir.
        :param out_extension: Documentation: https://esbuild.github.io/api/#out-extension.
        :param outfile: Documentation: https://esbuild.github.io/api/#outfile.
        :param packages: Documentation: https://esbuild.github.io/api/#packages.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param preserve_symlinks: Documentation: https://esbuild.github.io/api/#preserve-symlinks.
        :param public_path: Documentation: https://esbuild.github.io/api/#public-path.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param resolve_extensions: Documentation: https://esbuild.github.io/api/#resolve-extensions.
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param splitting: Documentation: https://esbuild.github.io/api/#splitting.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig: Documentation: https://esbuild.github.io/api/#tsconfig.
        :param write: Documentation: https://esbuild.github.io/api/#write.

        :throws: ``esbuild.BuildFailure``
        '''
        ...


class _IBuildProviderProxy:
    '''Provides an implementation of the esbuild Build API.'''

    __jsii_type__: typing.ClassVar[str] = "@mrgrain/cdk-esbuild.IBuildProvider"

    @jsii.member(jsii_name="buildSync")
    def build_sync(
        self,
        *,
        entry_points: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]]] = None,
        abs_working_dir: typing.Optional[builtins.str] = None,
        alias: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allow_overwrite: typing.Optional[builtins.bool] = None,
        asset_names: typing.Optional[builtins.str] = None,
        banner: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bundle: typing.Optional[builtins.bool] = None,
        charset: typing.Optional[builtins.str] = None,
        chunk_names: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        entry_names: typing.Optional[builtins.str] = None,
        external: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        inject: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        metafile: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        node_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbase: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        out_extension: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outfile: typing.Optional[builtins.str] = None,
        packages: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        preserve_symlinks: typing.Optional[builtins.bool] = None,
        public_path: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        resolve_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        splitting: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig: typing.Optional[builtins.str] = None,
        write: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''A method implementing the code build.

        During synth time, the method will receive all computed ``BuildOptions`` from the bundler.

        It MUST implement any output options to integrate correctly and MAY use any other options.
        On failure, it SHOULD print any warnings & errors to stderr and throw a ``BuildFailure`` to inform the bundler.

        :param entry_points: Documentation: https://esbuild.github.io/api/#entry-points.
        :param abs_working_dir: Documentation: https://esbuild.github.io/api/#working-directory.
        :param alias: Documentation: https://esbuild.github.io/api/#alias.
        :param allow_overwrite: Documentation: https://esbuild.github.io/api/#allow-overwrite.
        :param asset_names: Documentation: https://esbuild.github.io/api/#asset-names.
        :param banner: Documentation: https://esbuild.github.io/api/#banner.
        :param bundle: Documentation: https://esbuild.github.io/api/#bundle.
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param chunk_names: Documentation: https://esbuild.github.io/api/#chunk-names.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param conditions: Documentation: https://esbuild.github.io/api/#conditions.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param entry_names: Documentation: https://esbuild.github.io/api/#entry-names.
        :param external: Documentation: https://esbuild.github.io/api/#external.
        :param footer: Documentation: https://esbuild.github.io/api/#footer.
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param inject: Documentation: https://esbuild.github.io/api/#inject.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: Documentation: https://esbuild.github.io/api/#loader.
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param main_fields: Documentation: https://esbuild.github.io/api/#main-fields.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param metafile: Documentation: https://esbuild.github.io/api/#metafile.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param node_paths: Documentation: https://esbuild.github.io/api/#node-paths.
        :param outbase: Documentation: https://esbuild.github.io/api/#outbase.
        :param outdir: Documentation: https://esbuild.github.io/api/#outdir.
        :param out_extension: Documentation: https://esbuild.github.io/api/#out-extension.
        :param outfile: Documentation: https://esbuild.github.io/api/#outfile.
        :param packages: Documentation: https://esbuild.github.io/api/#packages.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param preserve_symlinks: Documentation: https://esbuild.github.io/api/#preserve-symlinks.
        :param public_path: Documentation: https://esbuild.github.io/api/#public-path.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param resolve_extensions: Documentation: https://esbuild.github.io/api/#resolve-extensions.
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param splitting: Documentation: https://esbuild.github.io/api/#splitting.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig: Documentation: https://esbuild.github.io/api/#tsconfig.
        :param write: Documentation: https://esbuild.github.io/api/#write.

        :throws: ``esbuild.BuildFailure``
        '''
        options = ProviderBuildOptions(
            entry_points=entry_points,
            abs_working_dir=abs_working_dir,
            alias=alias,
            allow_overwrite=allow_overwrite,
            asset_names=asset_names,
            banner=banner,
            bundle=bundle,
            charset=charset,
            chunk_names=chunk_names,
            color=color,
            conditions=conditions,
            define=define,
            drop=drop,
            entry_names=entry_names,
            external=external,
            footer=footer,
            format=format,
            global_name=global_name,
            ignore_annotations=ignore_annotations,
            inject=inject,
            jsx=jsx,
            jsx_dev=jsx_dev,
            jsx_factory=jsx_factory,
            jsx_fragment=jsx_fragment,
            jsx_import_source=jsx_import_source,
            jsx_side_effects=jsx_side_effects,
            keep_names=keep_names,
            legal_comments=legal_comments,
            loader=loader,
            log_level=log_level,
            log_limit=log_limit,
            log_override=log_override,
            main_fields=main_fields,
            mangle_cache=mangle_cache,
            mangle_props=mangle_props,
            mangle_quoted=mangle_quoted,
            metafile=metafile,
            minify=minify,
            minify_identifiers=minify_identifiers,
            minify_syntax=minify_syntax,
            minify_whitespace=minify_whitespace,
            node_paths=node_paths,
            outbase=outbase,
            outdir=outdir,
            out_extension=out_extension,
            outfile=outfile,
            packages=packages,
            platform=platform,
            preserve_symlinks=preserve_symlinks,
            public_path=public_path,
            pure=pure,
            reserve_props=reserve_props,
            resolve_extensions=resolve_extensions,
            sourcemap=sourcemap,
            source_root=source_root,
            sources_content=sources_content,
            splitting=splitting,
            supported=supported,
            target=target,
            tree_shaking=tree_shaking,
            tsconfig=tsconfig,
            write=write,
        )

        return typing.cast(None, jsii.invoke(self, "buildSync", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBuildProvider).__jsii_proxy_class__ = lambda : _IBuildProviderProxy


@jsii.interface(jsii_type="@mrgrain/cdk-esbuild.ITransformProvider")
class ITransformProvider(typing_extensions.Protocol):
    '''Provides an implementation of the esbuild Transform API.'''

    @jsii.member(jsii_name="transformSync")
    def transform_sync(
        self,
        input: builtins.str,
        *,
        banner: typing.Optional[builtins.str] = None,
        charset: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        platform: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        sourcefile: typing.Optional[builtins.str] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union["TsconfigOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> builtins.str:
        '''A method implementing the inline code transformation.

        During synth time, the method will receive the inline code and all computed ``TransformOptions`` from the bundler.

        MUST return the transformed code as a string to integrate correctly.
        It MAY use these options to do so.
        On failure, it SHOULD print any warnings & errors to stderr and throw a ``TransformFailure`` to inform the bundler.

        :param input: -
        :param banner: 
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param footer: 
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: 
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param sourcefile: 
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig_raw: 

        :throws: ``esbuild.TransformFailure``
        '''
        ...


class _ITransformProviderProxy:
    '''Provides an implementation of the esbuild Transform API.'''

    __jsii_type__: typing.ClassVar[str] = "@mrgrain/cdk-esbuild.ITransformProvider"

    @jsii.member(jsii_name="transformSync")
    def transform_sync(
        self,
        input: builtins.str,
        *,
        banner: typing.Optional[builtins.str] = None,
        charset: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        platform: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        sourcefile: typing.Optional[builtins.str] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union["TsconfigOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> builtins.str:
        '''A method implementing the inline code transformation.

        During synth time, the method will receive the inline code and all computed ``TransformOptions`` from the bundler.

        MUST return the transformed code as a string to integrate correctly.
        It MAY use these options to do so.
        On failure, it SHOULD print any warnings & errors to stderr and throw a ``TransformFailure`` to inform the bundler.

        :param input: -
        :param banner: 
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param footer: 
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: 
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param sourcefile: 
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig_raw: 

        :throws: ``esbuild.TransformFailure``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b273d64922e32225c024bddb7c08e70f30648e2537ff966572dee3fd5267a11d)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
        options = ProviderTransformOptions(
            banner=banner,
            charset=charset,
            color=color,
            define=define,
            drop=drop,
            footer=footer,
            format=format,
            global_name=global_name,
            ignore_annotations=ignore_annotations,
            jsx=jsx,
            jsx_dev=jsx_dev,
            jsx_factory=jsx_factory,
            jsx_fragment=jsx_fragment,
            jsx_import_source=jsx_import_source,
            jsx_side_effects=jsx_side_effects,
            keep_names=keep_names,
            legal_comments=legal_comments,
            loader=loader,
            log_level=log_level,
            log_limit=log_limit,
            log_override=log_override,
            mangle_cache=mangle_cache,
            mangle_props=mangle_props,
            mangle_quoted=mangle_quoted,
            minify=minify,
            minify_identifiers=minify_identifiers,
            minify_syntax=minify_syntax,
            minify_whitespace=minify_whitespace,
            platform=platform,
            pure=pure,
            reserve_props=reserve_props,
            sourcefile=sourcefile,
            sourcemap=sourcemap,
            source_root=source_root,
            sources_content=sources_content,
            supported=supported,
            target=target,
            tree_shaking=tree_shaking,
            tsconfig_raw=tsconfig_raw,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "transformSync", [input, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITransformProvider).__jsii_proxy_class__ = lambda : _ITransformProviderProxy


class InlineJavaScriptCode(
    _aws_cdk_aws_lambda_ceddda9d.InlineCode,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.InlineJavaScriptCode",
):
    '''An implementation of ``lambda.InlineCode`` using the esbuild Transform API. Inline function code is limited to 4 KiB after transformation.'''

    def __init__(
        self,
        code: builtins.str,
        *,
        transform_options: typing.Optional[typing.Union["TransformOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        transform_provider: typing.Optional[ITransformProvider] = None,
    ) -> None:
        '''
        :param code: The inline code to be transformed.
        :param transform_options: Transform options passed on to esbuild. Please refer to the esbuild Transform API docs for details.
        :param transform_provider: The esbuild Transform API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``ITransformProvider`` as an escape hatch. Default: new DefaultEsbuildProvider()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc33593af0b89f946131db30a4d4de49eb78d91ea1bef57c8fa9913c4c293dd1)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        props = TransformerProps(
            transform_options=transform_options, transform_provider=transform_provider
        )

        jsii.create(self.__class__, self, [code, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_lambda_ceddda9d.CodeConfig:
        '''Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9288df5c915db457b11d8163428843817b6ab36000054de4834cb9ae4a303c3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.CodeConfig, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> builtins.bool:
        '''Determines whether this Code is inline code or not.'''
        return typing.cast(builtins.bool, jsii.get(self, "isInline"))


class InlineTypeScriptCode(
    _aws_cdk_aws_lambda_ceddda9d.InlineCode,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.InlineTypeScriptCode",
):
    '''An implementation of ``lambda.InlineCode`` using the esbuild Transform API. Inline function code is limited to 4 KiB after transformation.'''

    def __init__(
        self,
        code: builtins.str,
        *,
        transform_options: typing.Optional[typing.Union["TransformOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        transform_provider: typing.Optional[ITransformProvider] = None,
    ) -> None:
        '''
        :param code: The inline code to be transformed.
        :param transform_options: Transform options passed on to esbuild. Please refer to the esbuild Transform API docs for details.
        :param transform_provider: The esbuild Transform API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``ITransformProvider`` as an escape hatch. Default: new DefaultEsbuildProvider()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5bcf0c5b4e074edf1efe7b546b2d926e6c963fbeeebf952ffca5ea0fd7127b)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        props = TransformerProps(
            transform_options=transform_options, transform_provider=transform_provider
        )

        jsii.create(self.__class__, self, [code, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_lambda_ceddda9d.CodeConfig:
        '''Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b8bec45384b1a113e49dc5131a885afb8dd52c5a5dcd74ca0ea30842102152)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.CodeConfig, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> builtins.bool:
        '''Determines whether this Code is inline code or not.'''
        return typing.cast(builtins.bool, jsii.get(self, "isInline"))


class JavaScriptAsset(
    EsbuildAsset,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.JavaScriptAsset",
):
    '''Bundles the entry points and creates a CDK asset which is uploaded to the bootstrapped CDK S3 bucket during deployment.

    The asset can be used by other constructs.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        asset_hash: typing.Optional[builtins.str] = None,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7c293653fc1a46e989f4190de1177ebd3f68affe07df2ac666fa2b3e58e333)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssetProps(
            entry_points=entry_points,
            asset_hash=asset_hash,
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class JavaScriptCode(
    EsbuildCode,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.JavaScriptCode",
):
    '''Represents the deployed JavaScript Code.'''

    def __init__(
        self,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4507163c84c56eb03714049d2f473f23bb8125c0f86941f81f35bee2ef4ae03f)
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
        props = JavaScriptCodeProps(
            asset_hash=asset_hash,
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [entry_points, props])

    @jsii.member(jsii_name="getAsset")
    def _get_asset(self, scope: _constructs_77d1e7e8.Construct) -> EsbuildAsset:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c44ce71d85c7855ea5a1a555e7ea52d13c85f740db1d0666f73c81fcedac3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(EsbuildAsset, jsii.invoke(self, "getAsset", [scope]))


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.JavaScriptCodeProps",
    jsii_struct_bases=[BundlerProps],
    name_mapping={
        "build_options": "buildOptions",
        "build_provider": "buildProvider",
        "copy_dir": "copyDir",
        "asset_hash": "assetHash",
    },
)
class JavaScriptCodeProps(BundlerProps):
    def __init__(
        self,
        *,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
        asset_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        '''
        if isinstance(build_options, dict):
            build_options = BuildOptions(**build_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f39896c298a9022e4c74318bcdd866488de29ae5dbc273a816eaaa87877471)
            check_type(argname="argument build_options", value=build_options, expected_type=type_hints["build_options"])
            check_type(argname="argument build_provider", value=build_provider, expected_type=type_hints["build_provider"])
            check_type(argname="argument copy_dir", value=copy_dir, expected_type=type_hints["copy_dir"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_options is not None:
            self._values["build_options"] = build_options
        if build_provider is not None:
            self._values["build_provider"] = build_provider
        if copy_dir is not None:
            self._values["copy_dir"] = copy_dir
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash

    @builtins.property
    def build_options(self) -> typing.Optional[BuildOptions]:
        '''Build options passed on to esbuild. Please refer to the esbuild Build API docs for details.

        - ``buildOptions.outdir: string``
          The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory.
          For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory.
          *Cannot be used together with ``outfile``*.
        - ``buildOptions.outfile: string``
          Relative path to a file inside the CDK asset output directory.
          For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point.
          *Cannot be used with multiple entryPoints or together with ``outdir``.*
        - ``buildOptions.absWorkingDir: string``
          Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_.
          If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).

        :see: https://esbuild.github.io/api/#build-api
        '''
        result = self._values.get("build_options")
        return typing.cast(typing.Optional[BuildOptions], result)

    @builtins.property
    def build_provider(self) -> typing.Optional[IBuildProvider]:
        '''The esbuild Build API implementation to be used.

        Configure the default ``EsbuildProvider`` for more options or
        provide a custom ``IBuildProvider`` as an escape hatch.

        :default: new EsbuildProvider()
        '''
        result = self._values.get("build_provider")
        return typing.cast(typing.Optional[IBuildProvider], result)

    @builtins.property
    def copy_dir(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]]:
        '''Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs.

        - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory.
        - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied.

        Therefore the following values for ``copyDir`` are all equivalent::

           { copyDir: "path/to/source" }
           { copyDir: ["path/to/source"] }
           { copyDir: { ".": "path/to/source" } }
           { copyDir: { ".": ["path/to/source"] } }

        The destination cannot be outside of the asset staging directory.
        If you are receiving the error "Cannot copy files to outside of the asset staging directory."
        you are likely using ``..`` or an absolute path as key on the ``copyDir`` map.
        Instead use only relative paths and avoid ``..``.
        '''
        result = self._values.get("copy_dir")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''A hash of this asset, which is available at construction time.

        As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed.

        Defaults to a hash of all files in the resulting bundle.
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JavaScriptCodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_s3_deployment_ceddda9d.ISource)
class JavaScriptSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.JavaScriptSource",
):
    def __init__(
        self,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3f50e082743d1d9113eaf78a36a88b8dc154cac77a4209408270009380d4d0)
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
        props = JavaScriptSourceProps(
            asset_hash=asset_hash,
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [entry_points, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        handler_role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> _aws_cdk_aws_s3_deployment_ceddda9d.SourceConfig:
        '''Binds the source to a bucket deployment.

        :param scope: -
        :param handler_role: The role for the handler.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf351b7981d89943eaea281c4e34aa55c78d9b4eb9849cf0bc84d50da8978ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = _aws_cdk_aws_s3_deployment_ceddda9d.DeploymentSourceContext(
            handler_role=handler_role
        )

        return typing.cast(_aws_cdk_aws_s3_deployment_ceddda9d.SourceConfig, jsii.invoke(self, "bind", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="asset")
    def _asset(self) -> typing.Union[JavaScriptAsset, "TypeScriptAsset"]:
        return typing.cast(typing.Union[JavaScriptAsset, "TypeScriptAsset"], jsii.get(self, "asset"))

    @_asset.setter
    def _asset(self, value: typing.Union[JavaScriptAsset, "TypeScriptAsset"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e925b32744da90e03880eb9891bd0bf67942f59132c9c137e75f4f408ab40b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asset", value)

    @builtins.property
    @jsii.member(jsii_name="assetClass")
    def asset_class(self) -> JavaScriptAsset:
        return typing.cast(JavaScriptAsset, jsii.get(self, "assetClass"))

    @asset_class.setter
    def asset_class(self, value: JavaScriptAsset) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e346f65f14043eddc497c05af00b110f5b6e76cd9760d9b60e2d4ea8a2fb7c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetClass", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "AssetProps":
        return typing.cast("AssetProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "AssetProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bcb9cb4f34df2e08980b0a37ea87e5c6f31e5450ac3460c110730703dceeba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.JavaScriptSourceProps",
    jsii_struct_bases=[BundlerProps],
    name_mapping={
        "build_options": "buildOptions",
        "build_provider": "buildProvider",
        "copy_dir": "copyDir",
        "asset_hash": "assetHash",
    },
)
class JavaScriptSourceProps(BundlerProps):
    def __init__(
        self,
        *,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
        asset_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        '''
        if isinstance(build_options, dict):
            build_options = BuildOptions(**build_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ef31d1935b5233ddb314ca48b282282a07491a73aaa68ada8337da1d10b4b6)
            check_type(argname="argument build_options", value=build_options, expected_type=type_hints["build_options"])
            check_type(argname="argument build_provider", value=build_provider, expected_type=type_hints["build_provider"])
            check_type(argname="argument copy_dir", value=copy_dir, expected_type=type_hints["copy_dir"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_options is not None:
            self._values["build_options"] = build_options
        if build_provider is not None:
            self._values["build_provider"] = build_provider
        if copy_dir is not None:
            self._values["copy_dir"] = copy_dir
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash

    @builtins.property
    def build_options(self) -> typing.Optional[BuildOptions]:
        '''Build options passed on to esbuild. Please refer to the esbuild Build API docs for details.

        - ``buildOptions.outdir: string``
          The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory.
          For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory.
          *Cannot be used together with ``outfile``*.
        - ``buildOptions.outfile: string``
          Relative path to a file inside the CDK asset output directory.
          For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point.
          *Cannot be used with multiple entryPoints or together with ``outdir``.*
        - ``buildOptions.absWorkingDir: string``
          Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_.
          If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).

        :see: https://esbuild.github.io/api/#build-api
        '''
        result = self._values.get("build_options")
        return typing.cast(typing.Optional[BuildOptions], result)

    @builtins.property
    def build_provider(self) -> typing.Optional[IBuildProvider]:
        '''The esbuild Build API implementation to be used.

        Configure the default ``EsbuildProvider`` for more options or
        provide a custom ``IBuildProvider`` as an escape hatch.

        :default: new EsbuildProvider()
        '''
        result = self._values.get("build_provider")
        return typing.cast(typing.Optional[IBuildProvider], result)

    @builtins.property
    def copy_dir(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]]:
        '''Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs.

        - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory.
        - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied.

        Therefore the following values for ``copyDir`` are all equivalent::

           { copyDir: "path/to/source" }
           { copyDir: ["path/to/source"] }
           { copyDir: { ".": "path/to/source" } }
           { copyDir: { ".": ["path/to/source"] } }

        The destination cannot be outside of the asset staging directory.
        If you are receiving the error "Cannot copy files to outside of the asset staging directory."
        you are likely using ``..`` or an absolute path as key on the ``copyDir`` map.
        Instead use only relative paths and avoid ``..``.
        '''
        result = self._values.get("copy_dir")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''A hash of this asset, which is available at construction time.

        As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed.

        Defaults to a hash of all files in the resulting bundle.
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JavaScriptSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.ProviderBuildOptions",
    jsii_struct_bases=[BuildOptions],
    name_mapping={
        "abs_working_dir": "absWorkingDir",
        "alias": "alias",
        "allow_overwrite": "allowOverwrite",
        "asset_names": "assetNames",
        "banner": "banner",
        "bundle": "bundle",
        "charset": "charset",
        "chunk_names": "chunkNames",
        "color": "color",
        "conditions": "conditions",
        "define": "define",
        "drop": "drop",
        "entry_names": "entryNames",
        "external": "external",
        "footer": "footer",
        "format": "format",
        "global_name": "globalName",
        "ignore_annotations": "ignoreAnnotations",
        "inject": "inject",
        "jsx": "jsx",
        "jsx_dev": "jsxDev",
        "jsx_factory": "jsxFactory",
        "jsx_fragment": "jsxFragment",
        "jsx_import_source": "jsxImportSource",
        "jsx_side_effects": "jsxSideEffects",
        "keep_names": "keepNames",
        "legal_comments": "legalComments",
        "loader": "loader",
        "log_level": "logLevel",
        "log_limit": "logLimit",
        "log_override": "logOverride",
        "main_fields": "mainFields",
        "mangle_cache": "mangleCache",
        "mangle_props": "mangleProps",
        "mangle_quoted": "mangleQuoted",
        "metafile": "metafile",
        "minify": "minify",
        "minify_identifiers": "minifyIdentifiers",
        "minify_syntax": "minifySyntax",
        "minify_whitespace": "minifyWhitespace",
        "node_paths": "nodePaths",
        "outbase": "outbase",
        "outdir": "outdir",
        "out_extension": "outExtension",
        "outfile": "outfile",
        "packages": "packages",
        "platform": "platform",
        "preserve_symlinks": "preserveSymlinks",
        "public_path": "publicPath",
        "pure": "pure",
        "reserve_props": "reserveProps",
        "resolve_extensions": "resolveExtensions",
        "sourcemap": "sourcemap",
        "source_root": "sourceRoot",
        "sources_content": "sourcesContent",
        "splitting": "splitting",
        "supported": "supported",
        "target": "target",
        "tree_shaking": "treeShaking",
        "tsconfig": "tsconfig",
        "write": "write",
        "entry_points": "entryPoints",
    },
)
class ProviderBuildOptions(BuildOptions):
    def __init__(
        self,
        *,
        abs_working_dir: typing.Optional[builtins.str] = None,
        alias: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allow_overwrite: typing.Optional[builtins.bool] = None,
        asset_names: typing.Optional[builtins.str] = None,
        banner: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bundle: typing.Optional[builtins.bool] = None,
        charset: typing.Optional[builtins.str] = None,
        chunk_names: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        entry_names: typing.Optional[builtins.str] = None,
        external: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        inject: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        metafile: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        node_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbase: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        out_extension: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outfile: typing.Optional[builtins.str] = None,
        packages: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        preserve_symlinks: typing.Optional[builtins.bool] = None,
        public_path: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        resolve_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        splitting: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig: typing.Optional[builtins.str] = None,
        write: typing.Optional[builtins.bool] = None,
        entry_points: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''
        :param abs_working_dir: Documentation: https://esbuild.github.io/api/#working-directory.
        :param alias: Documentation: https://esbuild.github.io/api/#alias.
        :param allow_overwrite: Documentation: https://esbuild.github.io/api/#allow-overwrite.
        :param asset_names: Documentation: https://esbuild.github.io/api/#asset-names.
        :param banner: Documentation: https://esbuild.github.io/api/#banner.
        :param bundle: Documentation: https://esbuild.github.io/api/#bundle.
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param chunk_names: Documentation: https://esbuild.github.io/api/#chunk-names.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param conditions: Documentation: https://esbuild.github.io/api/#conditions.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param entry_names: Documentation: https://esbuild.github.io/api/#entry-names.
        :param external: Documentation: https://esbuild.github.io/api/#external.
        :param footer: Documentation: https://esbuild.github.io/api/#footer.
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param inject: Documentation: https://esbuild.github.io/api/#inject.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: Documentation: https://esbuild.github.io/api/#loader.
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param main_fields: Documentation: https://esbuild.github.io/api/#main-fields.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param metafile: Documentation: https://esbuild.github.io/api/#metafile.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param node_paths: Documentation: https://esbuild.github.io/api/#node-paths.
        :param outbase: Documentation: https://esbuild.github.io/api/#outbase.
        :param outdir: Documentation: https://esbuild.github.io/api/#outdir.
        :param out_extension: Documentation: https://esbuild.github.io/api/#out-extension.
        :param outfile: Documentation: https://esbuild.github.io/api/#outfile.
        :param packages: Documentation: https://esbuild.github.io/api/#packages.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param preserve_symlinks: Documentation: https://esbuild.github.io/api/#preserve-symlinks.
        :param public_path: Documentation: https://esbuild.github.io/api/#public-path.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param resolve_extensions: Documentation: https://esbuild.github.io/api/#resolve-extensions.
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param splitting: Documentation: https://esbuild.github.io/api/#splitting.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig: Documentation: https://esbuild.github.io/api/#tsconfig.
        :param write: Documentation: https://esbuild.github.io/api/#write.
        :param entry_points: Documentation: https://esbuild.github.io/api/#entry-points.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78e7efccee59986fec35d76ced509c566ac34900b09d44551f2407cbf1cff4b)
            check_type(argname="argument abs_working_dir", value=abs_working_dir, expected_type=type_hints["abs_working_dir"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_overwrite", value=allow_overwrite, expected_type=type_hints["allow_overwrite"])
            check_type(argname="argument asset_names", value=asset_names, expected_type=type_hints["asset_names"])
            check_type(argname="argument banner", value=banner, expected_type=type_hints["banner"])
            check_type(argname="argument bundle", value=bundle, expected_type=type_hints["bundle"])
            check_type(argname="argument charset", value=charset, expected_type=type_hints["charset"])
            check_type(argname="argument chunk_names", value=chunk_names, expected_type=type_hints["chunk_names"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument define", value=define, expected_type=type_hints["define"])
            check_type(argname="argument drop", value=drop, expected_type=type_hints["drop"])
            check_type(argname="argument entry_names", value=entry_names, expected_type=type_hints["entry_names"])
            check_type(argname="argument external", value=external, expected_type=type_hints["external"])
            check_type(argname="argument footer", value=footer, expected_type=type_hints["footer"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument global_name", value=global_name, expected_type=type_hints["global_name"])
            check_type(argname="argument ignore_annotations", value=ignore_annotations, expected_type=type_hints["ignore_annotations"])
            check_type(argname="argument inject", value=inject, expected_type=type_hints["inject"])
            check_type(argname="argument jsx", value=jsx, expected_type=type_hints["jsx"])
            check_type(argname="argument jsx_dev", value=jsx_dev, expected_type=type_hints["jsx_dev"])
            check_type(argname="argument jsx_factory", value=jsx_factory, expected_type=type_hints["jsx_factory"])
            check_type(argname="argument jsx_fragment", value=jsx_fragment, expected_type=type_hints["jsx_fragment"])
            check_type(argname="argument jsx_import_source", value=jsx_import_source, expected_type=type_hints["jsx_import_source"])
            check_type(argname="argument jsx_side_effects", value=jsx_side_effects, expected_type=type_hints["jsx_side_effects"])
            check_type(argname="argument keep_names", value=keep_names, expected_type=type_hints["keep_names"])
            check_type(argname="argument legal_comments", value=legal_comments, expected_type=type_hints["legal_comments"])
            check_type(argname="argument loader", value=loader, expected_type=type_hints["loader"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument log_limit", value=log_limit, expected_type=type_hints["log_limit"])
            check_type(argname="argument log_override", value=log_override, expected_type=type_hints["log_override"])
            check_type(argname="argument main_fields", value=main_fields, expected_type=type_hints["main_fields"])
            check_type(argname="argument mangle_cache", value=mangle_cache, expected_type=type_hints["mangle_cache"])
            check_type(argname="argument mangle_props", value=mangle_props, expected_type=type_hints["mangle_props"])
            check_type(argname="argument mangle_quoted", value=mangle_quoted, expected_type=type_hints["mangle_quoted"])
            check_type(argname="argument metafile", value=metafile, expected_type=type_hints["metafile"])
            check_type(argname="argument minify", value=minify, expected_type=type_hints["minify"])
            check_type(argname="argument minify_identifiers", value=minify_identifiers, expected_type=type_hints["minify_identifiers"])
            check_type(argname="argument minify_syntax", value=minify_syntax, expected_type=type_hints["minify_syntax"])
            check_type(argname="argument minify_whitespace", value=minify_whitespace, expected_type=type_hints["minify_whitespace"])
            check_type(argname="argument node_paths", value=node_paths, expected_type=type_hints["node_paths"])
            check_type(argname="argument outbase", value=outbase, expected_type=type_hints["outbase"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument out_extension", value=out_extension, expected_type=type_hints["out_extension"])
            check_type(argname="argument outfile", value=outfile, expected_type=type_hints["outfile"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument preserve_symlinks", value=preserve_symlinks, expected_type=type_hints["preserve_symlinks"])
            check_type(argname="argument public_path", value=public_path, expected_type=type_hints["public_path"])
            check_type(argname="argument pure", value=pure, expected_type=type_hints["pure"])
            check_type(argname="argument reserve_props", value=reserve_props, expected_type=type_hints["reserve_props"])
            check_type(argname="argument resolve_extensions", value=resolve_extensions, expected_type=type_hints["resolve_extensions"])
            check_type(argname="argument sourcemap", value=sourcemap, expected_type=type_hints["sourcemap"])
            check_type(argname="argument source_root", value=source_root, expected_type=type_hints["source_root"])
            check_type(argname="argument sources_content", value=sources_content, expected_type=type_hints["sources_content"])
            check_type(argname="argument splitting", value=splitting, expected_type=type_hints["splitting"])
            check_type(argname="argument supported", value=supported, expected_type=type_hints["supported"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument tree_shaking", value=tree_shaking, expected_type=type_hints["tree_shaking"])
            check_type(argname="argument tsconfig", value=tsconfig, expected_type=type_hints["tsconfig"])
            check_type(argname="argument write", value=write, expected_type=type_hints["write"])
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if abs_working_dir is not None:
            self._values["abs_working_dir"] = abs_working_dir
        if alias is not None:
            self._values["alias"] = alias
        if allow_overwrite is not None:
            self._values["allow_overwrite"] = allow_overwrite
        if asset_names is not None:
            self._values["asset_names"] = asset_names
        if banner is not None:
            self._values["banner"] = banner
        if bundle is not None:
            self._values["bundle"] = bundle
        if charset is not None:
            self._values["charset"] = charset
        if chunk_names is not None:
            self._values["chunk_names"] = chunk_names
        if color is not None:
            self._values["color"] = color
        if conditions is not None:
            self._values["conditions"] = conditions
        if define is not None:
            self._values["define"] = define
        if drop is not None:
            self._values["drop"] = drop
        if entry_names is not None:
            self._values["entry_names"] = entry_names
        if external is not None:
            self._values["external"] = external
        if footer is not None:
            self._values["footer"] = footer
        if format is not None:
            self._values["format"] = format
        if global_name is not None:
            self._values["global_name"] = global_name
        if ignore_annotations is not None:
            self._values["ignore_annotations"] = ignore_annotations
        if inject is not None:
            self._values["inject"] = inject
        if jsx is not None:
            self._values["jsx"] = jsx
        if jsx_dev is not None:
            self._values["jsx_dev"] = jsx_dev
        if jsx_factory is not None:
            self._values["jsx_factory"] = jsx_factory
        if jsx_fragment is not None:
            self._values["jsx_fragment"] = jsx_fragment
        if jsx_import_source is not None:
            self._values["jsx_import_source"] = jsx_import_source
        if jsx_side_effects is not None:
            self._values["jsx_side_effects"] = jsx_side_effects
        if keep_names is not None:
            self._values["keep_names"] = keep_names
        if legal_comments is not None:
            self._values["legal_comments"] = legal_comments
        if loader is not None:
            self._values["loader"] = loader
        if log_level is not None:
            self._values["log_level"] = log_level
        if log_limit is not None:
            self._values["log_limit"] = log_limit
        if log_override is not None:
            self._values["log_override"] = log_override
        if main_fields is not None:
            self._values["main_fields"] = main_fields
        if mangle_cache is not None:
            self._values["mangle_cache"] = mangle_cache
        if mangle_props is not None:
            self._values["mangle_props"] = mangle_props
        if mangle_quoted is not None:
            self._values["mangle_quoted"] = mangle_quoted
        if metafile is not None:
            self._values["metafile"] = metafile
        if minify is not None:
            self._values["minify"] = minify
        if minify_identifiers is not None:
            self._values["minify_identifiers"] = minify_identifiers
        if minify_syntax is not None:
            self._values["minify_syntax"] = minify_syntax
        if minify_whitespace is not None:
            self._values["minify_whitespace"] = minify_whitespace
        if node_paths is not None:
            self._values["node_paths"] = node_paths
        if outbase is not None:
            self._values["outbase"] = outbase
        if outdir is not None:
            self._values["outdir"] = outdir
        if out_extension is not None:
            self._values["out_extension"] = out_extension
        if outfile is not None:
            self._values["outfile"] = outfile
        if packages is not None:
            self._values["packages"] = packages
        if platform is not None:
            self._values["platform"] = platform
        if preserve_symlinks is not None:
            self._values["preserve_symlinks"] = preserve_symlinks
        if public_path is not None:
            self._values["public_path"] = public_path
        if pure is not None:
            self._values["pure"] = pure
        if reserve_props is not None:
            self._values["reserve_props"] = reserve_props
        if resolve_extensions is not None:
            self._values["resolve_extensions"] = resolve_extensions
        if sourcemap is not None:
            self._values["sourcemap"] = sourcemap
        if source_root is not None:
            self._values["source_root"] = source_root
        if sources_content is not None:
            self._values["sources_content"] = sources_content
        if splitting is not None:
            self._values["splitting"] = splitting
        if supported is not None:
            self._values["supported"] = supported
        if target is not None:
            self._values["target"] = target
        if tree_shaking is not None:
            self._values["tree_shaking"] = tree_shaking
        if tsconfig is not None:
            self._values["tsconfig"] = tsconfig
        if write is not None:
            self._values["write"] = write
        if entry_points is not None:
            self._values["entry_points"] = entry_points

    @builtins.property
    def abs_working_dir(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#working-directory.'''
        result = self._values.get("abs_working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#alias.'''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def allow_overwrite(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#allow-overwrite.'''
        result = self._values.get("allow_overwrite")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def asset_names(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#asset-names.'''
        result = self._values.get("asset_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def banner(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#banner.'''
        result = self._values.get("banner")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bundle(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#bundle.'''
        result = self._values.get("bundle")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def charset(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#charset.'''
        result = self._values.get("charset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chunk_names(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#chunk-names.'''
        result = self._values.get("chunk_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#color.'''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#conditions.'''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def define(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#define.'''
        result = self._values.get("define")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def drop(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#drop.'''
        result = self._values.get("drop")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entry_names(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#entry-names.'''
        result = self._values.get("entry_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#external.'''
        result = self._values.get("external")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def footer(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#footer.'''
        result = self._values.get("footer")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#format.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_name(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#global-name.'''
        result = self._values.get("global_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_annotations(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#ignore-annotations.'''
        result = self._values.get("ignore_annotations")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def inject(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#inject.'''
        result = self._values.get("inject")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jsx(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx.'''
        result = self._values.get("jsx")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_dev(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-development.'''
        result = self._values.get("jsx_dev")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx_factory(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-factory.'''
        result = self._values.get("jsx_factory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_fragment(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-fragment.'''
        result = self._values.get("jsx_fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_import_source(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-import-source.'''
        result = self._values.get("jsx_import_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_side_effects(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-side-effects.'''
        result = self._values.get("jsx_side_effects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def keep_names(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#keep-names.'''
        result = self._values.get("keep_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def legal_comments(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#legal-comments.'''
        result = self._values.get("legal_comments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def loader(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#loader.'''
        result = self._values.get("loader")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#log-level.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_limit(self) -> typing.Optional[jsii.Number]:
        '''Documentation: https://esbuild.github.io/api/#log-limit.'''
        result = self._values.get("log_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_override(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#log-override.'''
        result = self._values.get("log_override")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def main_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#main-fields.'''
        result = self._values.get("main_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mangle_cache(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_cache")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]], result)

    @builtins.property
    def mangle_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def mangle_quoted(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_quoted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metafile(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#metafile.'''
        result = self._values.get("metafile")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_identifiers(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_identifiers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_syntax(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_syntax")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_whitespace(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_whitespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#node-paths.'''
        result = self._values.get("node_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outbase(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#outbase.'''
        result = self._values.get("outbase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#outdir.'''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def out_extension(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#out-extension.'''
        result = self._values.get("out_extension")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def outfile(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#outfile.'''
        result = self._values.get("outfile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#packages.'''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#platform.'''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_symlinks(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#preserve-symlinks.'''
        result = self._values.get("preserve_symlinks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def public_path(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#public-path.'''
        result = self._values.get("public_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pure(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#pure.'''
        result = self._values.get("pure")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reserve_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("reserve_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resolve_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#resolve-extensions.'''
        result = self._values.get("resolve_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sourcemap(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#sourcemap.'''
        result = self._values.get("sourcemap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], result)

    @builtins.property
    def source_root(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#source-root.'''
        result = self._values.get("source_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources_content(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#sources-content.'''
        result = self._values.get("sources_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def splitting(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#splitting.'''
        result = self._values.get("splitting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supported(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.bool]]:
        '''Documentation: https://esbuild.github.io/api/#supported.'''
        result = self._values.get("supported")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.bool]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''Documentation: https://esbuild.github.io/api/#target.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def tree_shaking(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#tree-shaking.'''
        result = self._values.get("tree_shaking")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tsconfig(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#tsconfig.'''
        result = self._values.get("tsconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def write(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#write.'''
        result = self._values.get("write")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def entry_points(
        self,
    ) -> typing.Optional[typing.Union[typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]]]:
        '''Documentation: https://esbuild.github.io/api/#entry-points.'''
        result = self._values.get("entry_points")
        return typing.cast(typing.Optional[typing.Union[typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.TransformOptions",
    jsii_struct_bases=[],
    name_mapping={
        "banner": "banner",
        "charset": "charset",
        "color": "color",
        "define": "define",
        "drop": "drop",
        "footer": "footer",
        "format": "format",
        "global_name": "globalName",
        "ignore_annotations": "ignoreAnnotations",
        "jsx": "jsx",
        "jsx_dev": "jsxDev",
        "jsx_factory": "jsxFactory",
        "jsx_fragment": "jsxFragment",
        "jsx_import_source": "jsxImportSource",
        "jsx_side_effects": "jsxSideEffects",
        "keep_names": "keepNames",
        "legal_comments": "legalComments",
        "loader": "loader",
        "log_level": "logLevel",
        "log_limit": "logLimit",
        "log_override": "logOverride",
        "mangle_cache": "mangleCache",
        "mangle_props": "mangleProps",
        "mangle_quoted": "mangleQuoted",
        "minify": "minify",
        "minify_identifiers": "minifyIdentifiers",
        "minify_syntax": "minifySyntax",
        "minify_whitespace": "minifyWhitespace",
        "platform": "platform",
        "pure": "pure",
        "reserve_props": "reserveProps",
        "sourcefile": "sourcefile",
        "sourcemap": "sourcemap",
        "source_root": "sourceRoot",
        "sources_content": "sourcesContent",
        "supported": "supported",
        "target": "target",
        "tree_shaking": "treeShaking",
        "tsconfig_raw": "tsconfigRaw",
    },
)
class TransformOptions:
    def __init__(
        self,
        *,
        banner: typing.Optional[builtins.str] = None,
        charset: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        platform: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        sourcefile: typing.Optional[builtins.str] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union["TsconfigOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param banner: 
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param footer: 
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: 
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param sourcefile: 
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig_raw: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c37248db4a858f2f46ff70ce7ec32f72b189492c09c9e26fc3552cb219fbd47)
            check_type(argname="argument banner", value=banner, expected_type=type_hints["banner"])
            check_type(argname="argument charset", value=charset, expected_type=type_hints["charset"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument define", value=define, expected_type=type_hints["define"])
            check_type(argname="argument drop", value=drop, expected_type=type_hints["drop"])
            check_type(argname="argument footer", value=footer, expected_type=type_hints["footer"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument global_name", value=global_name, expected_type=type_hints["global_name"])
            check_type(argname="argument ignore_annotations", value=ignore_annotations, expected_type=type_hints["ignore_annotations"])
            check_type(argname="argument jsx", value=jsx, expected_type=type_hints["jsx"])
            check_type(argname="argument jsx_dev", value=jsx_dev, expected_type=type_hints["jsx_dev"])
            check_type(argname="argument jsx_factory", value=jsx_factory, expected_type=type_hints["jsx_factory"])
            check_type(argname="argument jsx_fragment", value=jsx_fragment, expected_type=type_hints["jsx_fragment"])
            check_type(argname="argument jsx_import_source", value=jsx_import_source, expected_type=type_hints["jsx_import_source"])
            check_type(argname="argument jsx_side_effects", value=jsx_side_effects, expected_type=type_hints["jsx_side_effects"])
            check_type(argname="argument keep_names", value=keep_names, expected_type=type_hints["keep_names"])
            check_type(argname="argument legal_comments", value=legal_comments, expected_type=type_hints["legal_comments"])
            check_type(argname="argument loader", value=loader, expected_type=type_hints["loader"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument log_limit", value=log_limit, expected_type=type_hints["log_limit"])
            check_type(argname="argument log_override", value=log_override, expected_type=type_hints["log_override"])
            check_type(argname="argument mangle_cache", value=mangle_cache, expected_type=type_hints["mangle_cache"])
            check_type(argname="argument mangle_props", value=mangle_props, expected_type=type_hints["mangle_props"])
            check_type(argname="argument mangle_quoted", value=mangle_quoted, expected_type=type_hints["mangle_quoted"])
            check_type(argname="argument minify", value=minify, expected_type=type_hints["minify"])
            check_type(argname="argument minify_identifiers", value=minify_identifiers, expected_type=type_hints["minify_identifiers"])
            check_type(argname="argument minify_syntax", value=minify_syntax, expected_type=type_hints["minify_syntax"])
            check_type(argname="argument minify_whitespace", value=minify_whitespace, expected_type=type_hints["minify_whitespace"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument pure", value=pure, expected_type=type_hints["pure"])
            check_type(argname="argument reserve_props", value=reserve_props, expected_type=type_hints["reserve_props"])
            check_type(argname="argument sourcefile", value=sourcefile, expected_type=type_hints["sourcefile"])
            check_type(argname="argument sourcemap", value=sourcemap, expected_type=type_hints["sourcemap"])
            check_type(argname="argument source_root", value=source_root, expected_type=type_hints["source_root"])
            check_type(argname="argument sources_content", value=sources_content, expected_type=type_hints["sources_content"])
            check_type(argname="argument supported", value=supported, expected_type=type_hints["supported"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument tree_shaking", value=tree_shaking, expected_type=type_hints["tree_shaking"])
            check_type(argname="argument tsconfig_raw", value=tsconfig_raw, expected_type=type_hints["tsconfig_raw"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if banner is not None:
            self._values["banner"] = banner
        if charset is not None:
            self._values["charset"] = charset
        if color is not None:
            self._values["color"] = color
        if define is not None:
            self._values["define"] = define
        if drop is not None:
            self._values["drop"] = drop
        if footer is not None:
            self._values["footer"] = footer
        if format is not None:
            self._values["format"] = format
        if global_name is not None:
            self._values["global_name"] = global_name
        if ignore_annotations is not None:
            self._values["ignore_annotations"] = ignore_annotations
        if jsx is not None:
            self._values["jsx"] = jsx
        if jsx_dev is not None:
            self._values["jsx_dev"] = jsx_dev
        if jsx_factory is not None:
            self._values["jsx_factory"] = jsx_factory
        if jsx_fragment is not None:
            self._values["jsx_fragment"] = jsx_fragment
        if jsx_import_source is not None:
            self._values["jsx_import_source"] = jsx_import_source
        if jsx_side_effects is not None:
            self._values["jsx_side_effects"] = jsx_side_effects
        if keep_names is not None:
            self._values["keep_names"] = keep_names
        if legal_comments is not None:
            self._values["legal_comments"] = legal_comments
        if loader is not None:
            self._values["loader"] = loader
        if log_level is not None:
            self._values["log_level"] = log_level
        if log_limit is not None:
            self._values["log_limit"] = log_limit
        if log_override is not None:
            self._values["log_override"] = log_override
        if mangle_cache is not None:
            self._values["mangle_cache"] = mangle_cache
        if mangle_props is not None:
            self._values["mangle_props"] = mangle_props
        if mangle_quoted is not None:
            self._values["mangle_quoted"] = mangle_quoted
        if minify is not None:
            self._values["minify"] = minify
        if minify_identifiers is not None:
            self._values["minify_identifiers"] = minify_identifiers
        if minify_syntax is not None:
            self._values["minify_syntax"] = minify_syntax
        if minify_whitespace is not None:
            self._values["minify_whitespace"] = minify_whitespace
        if platform is not None:
            self._values["platform"] = platform
        if pure is not None:
            self._values["pure"] = pure
        if reserve_props is not None:
            self._values["reserve_props"] = reserve_props
        if sourcefile is not None:
            self._values["sourcefile"] = sourcefile
        if sourcemap is not None:
            self._values["sourcemap"] = sourcemap
        if source_root is not None:
            self._values["source_root"] = source_root
        if sources_content is not None:
            self._values["sources_content"] = sources_content
        if supported is not None:
            self._values["supported"] = supported
        if target is not None:
            self._values["target"] = target
        if tree_shaking is not None:
            self._values["tree_shaking"] = tree_shaking
        if tsconfig_raw is not None:
            self._values["tsconfig_raw"] = tsconfig_raw

    @builtins.property
    def banner(self) -> typing.Optional[builtins.str]:
        result = self._values.get("banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def charset(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#charset.'''
        result = self._values.get("charset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#color.'''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def define(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#define.'''
        result = self._values.get("define")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def drop(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#drop.'''
        result = self._values.get("drop")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def footer(self) -> typing.Optional[builtins.str]:
        result = self._values.get("footer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#format.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_name(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#global-name.'''
        result = self._values.get("global_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_annotations(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#ignore-annotations.'''
        result = self._values.get("ignore_annotations")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx.'''
        result = self._values.get("jsx")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_dev(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-development.'''
        result = self._values.get("jsx_dev")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx_factory(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-factory.'''
        result = self._values.get("jsx_factory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_fragment(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-fragment.'''
        result = self._values.get("jsx_fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_import_source(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-import-source.'''
        result = self._values.get("jsx_import_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_side_effects(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-side-effects.'''
        result = self._values.get("jsx_side_effects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def keep_names(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#keep-names.'''
        result = self._values.get("keep_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def legal_comments(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#legal-comments.'''
        result = self._values.get("legal_comments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def loader(self) -> typing.Optional[builtins.str]:
        result = self._values.get("loader")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#log-level.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_limit(self) -> typing.Optional[jsii.Number]:
        '''Documentation: https://esbuild.github.io/api/#log-limit.'''
        result = self._values.get("log_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_override(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#log-override.'''
        result = self._values.get("log_override")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mangle_cache(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_cache")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]], result)

    @builtins.property
    def mangle_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def mangle_quoted(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_quoted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_identifiers(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_identifiers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_syntax(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_syntax")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_whitespace(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_whitespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#platform.'''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pure(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#pure.'''
        result = self._values.get("pure")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reserve_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("reserve_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def sourcefile(self) -> typing.Optional[builtins.str]:
        result = self._values.get("sourcefile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sourcemap(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#sourcemap.'''
        result = self._values.get("sourcemap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], result)

    @builtins.property
    def source_root(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#source-root.'''
        result = self._values.get("source_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources_content(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#sources-content.'''
        result = self._values.get("sources_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supported(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.bool]]:
        '''Documentation: https://esbuild.github.io/api/#supported.'''
        result = self._values.get("supported")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.bool]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''Documentation: https://esbuild.github.io/api/#target.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def tree_shaking(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#tree-shaking.'''
        result = self._values.get("tree_shaking")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tsconfig_raw(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "TsconfigOptions"]]:
        result = self._values.get("tsconfig_raw")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "TsconfigOptions"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.TransformerProps",
    jsii_struct_bases=[],
    name_mapping={
        "transform_options": "transformOptions",
        "transform_provider": "transformProvider",
    },
)
class TransformerProps:
    def __init__(
        self,
        *,
        transform_options: typing.Optional[typing.Union[TransformOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        transform_provider: typing.Optional[ITransformProvider] = None,
    ) -> None:
        '''
        :param transform_options: Transform options passed on to esbuild. Please refer to the esbuild Transform API docs for details.
        :param transform_provider: The esbuild Transform API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``ITransformProvider`` as an escape hatch. Default: new DefaultEsbuildProvider()
        '''
        if isinstance(transform_options, dict):
            transform_options = TransformOptions(**transform_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc58b06985a425c97d91ff68cb5366f217b2e95fc05f434a2c8913993546369b)
            check_type(argname="argument transform_options", value=transform_options, expected_type=type_hints["transform_options"])
            check_type(argname="argument transform_provider", value=transform_provider, expected_type=type_hints["transform_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if transform_options is not None:
            self._values["transform_options"] = transform_options
        if transform_provider is not None:
            self._values["transform_provider"] = transform_provider

    @builtins.property
    def transform_options(self) -> typing.Optional[TransformOptions]:
        '''Transform options passed on to esbuild.

        Please refer to the esbuild Transform API docs for details.

        :see: https://esbuild.github.io/api/#transform-api
        '''
        result = self._values.get("transform_options")
        return typing.cast(typing.Optional[TransformOptions], result)

    @builtins.property
    def transform_provider(self) -> typing.Optional[ITransformProvider]:
        '''The esbuild Transform API implementation to be used.

        Configure the default ``EsbuildProvider`` for more options or
        provide a custom ``ITransformProvider`` as an escape hatch.

        :default: new DefaultEsbuildProvider()
        '''
        result = self._values.get("transform_provider")
        return typing.cast(typing.Optional[ITransformProvider], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.TsconfigOptions",
    jsii_struct_bases=[],
    name_mapping={"compiler_options": "compilerOptions"},
)
class TsconfigOptions:
    def __init__(
        self,
        *,
        compiler_options: typing.Optional[typing.Union[CompilerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param compiler_options: 
        '''
        if isinstance(compiler_options, dict):
            compiler_options = CompilerOptions(**compiler_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83734fd122d82939d2ffe79d063580419456cc543d3ed09342815c5d5803d460)
            check_type(argname="argument compiler_options", value=compiler_options, expected_type=type_hints["compiler_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compiler_options is not None:
            self._values["compiler_options"] = compiler_options

    @builtins.property
    def compiler_options(self) -> typing.Optional[CompilerOptions]:
        result = self._values.get("compiler_options")
        return typing.cast(typing.Optional[CompilerOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TsconfigOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TypeScriptAsset(
    EsbuildAsset,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.TypeScriptAsset",
):
    '''Bundles the entry points and creates a CDK asset which is uploaded to the bootstrapped CDK S3 bucket during deployment.

    The asset can be used by other constructs.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        asset_hash: typing.Optional[builtins.str] = None,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4b2df3385e42f976caa97a3cb710e87cff5020eb30f93ab0c57dd209f30e1d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssetProps(
            entry_points=entry_points,
            asset_hash=asset_hash,
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class TypeScriptCode(
    EsbuildCode,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.TypeScriptCode",
):
    '''Represents the deployed TypeScript Code.'''

    def __init__(
        self,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54aaf93a7fa033eebe7abbb99ce48fb8d394e94136697e90200b3c33c8c1e532)
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
        props = TypeScriptCodeProps(
            asset_hash=asset_hash,
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [entry_points, props])

    @jsii.member(jsii_name="getAsset")
    def _get_asset(self, scope: _constructs_77d1e7e8.Construct) -> EsbuildAsset:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91527f1d6303f104ddd5d7660026fd21b612b51f01a7fa06355c06e0af22d930)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(EsbuildAsset, jsii.invoke(self, "getAsset", [scope]))


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.TypeScriptCodeProps",
    jsii_struct_bases=[BundlerProps],
    name_mapping={
        "build_options": "buildOptions",
        "build_provider": "buildProvider",
        "copy_dir": "copyDir",
        "asset_hash": "assetHash",
    },
)
class TypeScriptCodeProps(BundlerProps):
    def __init__(
        self,
        *,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
        asset_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        '''
        if isinstance(build_options, dict):
            build_options = BuildOptions(**build_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57f845df99b12169ddd9f6ae8ea59cec6ef4a8067d9c4defe0d44270463afb7)
            check_type(argname="argument build_options", value=build_options, expected_type=type_hints["build_options"])
            check_type(argname="argument build_provider", value=build_provider, expected_type=type_hints["build_provider"])
            check_type(argname="argument copy_dir", value=copy_dir, expected_type=type_hints["copy_dir"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_options is not None:
            self._values["build_options"] = build_options
        if build_provider is not None:
            self._values["build_provider"] = build_provider
        if copy_dir is not None:
            self._values["copy_dir"] = copy_dir
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash

    @builtins.property
    def build_options(self) -> typing.Optional[BuildOptions]:
        '''Build options passed on to esbuild. Please refer to the esbuild Build API docs for details.

        - ``buildOptions.outdir: string``
          The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory.
          For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory.
          *Cannot be used together with ``outfile``*.
        - ``buildOptions.outfile: string``
          Relative path to a file inside the CDK asset output directory.
          For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point.
          *Cannot be used with multiple entryPoints or together with ``outdir``.*
        - ``buildOptions.absWorkingDir: string``
          Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_.
          If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).

        :see: https://esbuild.github.io/api/#build-api
        '''
        result = self._values.get("build_options")
        return typing.cast(typing.Optional[BuildOptions], result)

    @builtins.property
    def build_provider(self) -> typing.Optional[IBuildProvider]:
        '''The esbuild Build API implementation to be used.

        Configure the default ``EsbuildProvider`` for more options or
        provide a custom ``IBuildProvider`` as an escape hatch.

        :default: new EsbuildProvider()
        '''
        result = self._values.get("build_provider")
        return typing.cast(typing.Optional[IBuildProvider], result)

    @builtins.property
    def copy_dir(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]]:
        '''Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs.

        - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory.
        - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied.

        Therefore the following values for ``copyDir`` are all equivalent::

           { copyDir: "path/to/source" }
           { copyDir: ["path/to/source"] }
           { copyDir: { ".": "path/to/source" } }
           { copyDir: { ".": ["path/to/source"] } }

        The destination cannot be outside of the asset staging directory.
        If you are receiving the error "Cannot copy files to outside of the asset staging directory."
        you are likely using ``..`` or an absolute path as key on the ``copyDir`` map.
        Instead use only relative paths and avoid ``..``.
        '''
        result = self._values.get("copy_dir")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''A hash of this asset, which is available at construction time.

        As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed.

        Defaults to a hash of all files in the resulting bundle.
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TypeScriptCodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_s3_deployment_ceddda9d.ISource)
class TypeScriptSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.TypeScriptSource",
):
    def __init__(
        self,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    ) -> None:
        '''
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48105ed0b909a4fdfdc06c3ff865cce3202b96b81ee7be69e7617e62dcf1163)
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
        props = TypeScriptSourceProps(
            asset_hash=asset_hash,
            build_options=build_options,
            build_provider=build_provider,
            copy_dir=copy_dir,
        )

        jsii.create(self.__class__, self, [entry_points, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        handler_role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> _aws_cdk_aws_s3_deployment_ceddda9d.SourceConfig:
        '''Binds the source to a bucket deployment.

        :param scope: -
        :param handler_role: The role for the handler.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dbcbde63a5766d4de14a37346c050f53c31a267934171012ccc381663a8036c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = _aws_cdk_aws_s3_deployment_ceddda9d.DeploymentSourceContext(
            handler_role=handler_role
        )

        return typing.cast(_aws_cdk_aws_s3_deployment_ceddda9d.SourceConfig, jsii.invoke(self, "bind", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="asset")
    def _asset(self) -> typing.Union[JavaScriptAsset, TypeScriptAsset]:
        return typing.cast(typing.Union[JavaScriptAsset, TypeScriptAsset], jsii.get(self, "asset"))

    @_asset.setter
    def _asset(self, value: typing.Union[JavaScriptAsset, TypeScriptAsset]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a963a15411f9b48fcbd28a99bdfaa2b2f747bad253f6af021f01c0a89d696e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asset", value)

    @builtins.property
    @jsii.member(jsii_name="assetClass")
    def asset_class(self) -> TypeScriptAsset:
        return typing.cast(TypeScriptAsset, jsii.get(self, "assetClass"))

    @asset_class.setter
    def asset_class(self, value: TypeScriptAsset) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fcb1e5a2c95b154e98acdbb52b335f324a32fc76c045c77f7283ad8771105b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetClass", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "AssetProps":
        return typing.cast("AssetProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "AssetProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6926cc3b4983633d848a739a5b9e1f74d499f7d5cc41480cac8b0184dade76e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.TypeScriptSourceProps",
    jsii_struct_bases=[BundlerProps],
    name_mapping={
        "build_options": "buildOptions",
        "build_provider": "buildProvider",
        "copy_dir": "copyDir",
        "asset_hash": "assetHash",
    },
)
class TypeScriptSourceProps(BundlerProps):
    def __init__(
        self,
        *,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
        asset_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        '''
        if isinstance(build_options, dict):
            build_options = BuildOptions(**build_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269edc1e8ae899306e5ef7e6e60a5a9dc94d277d28a0a395bbb0dfd0eaa3e8f7)
            check_type(argname="argument build_options", value=build_options, expected_type=type_hints["build_options"])
            check_type(argname="argument build_provider", value=build_provider, expected_type=type_hints["build_provider"])
            check_type(argname="argument copy_dir", value=copy_dir, expected_type=type_hints["copy_dir"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_options is not None:
            self._values["build_options"] = build_options
        if build_provider is not None:
            self._values["build_provider"] = build_provider
        if copy_dir is not None:
            self._values["copy_dir"] = copy_dir
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash

    @builtins.property
    def build_options(self) -> typing.Optional[BuildOptions]:
        '''Build options passed on to esbuild. Please refer to the esbuild Build API docs for details.

        - ``buildOptions.outdir: string``
          The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory.
          For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory.
          *Cannot be used together with ``outfile``*.
        - ``buildOptions.outfile: string``
          Relative path to a file inside the CDK asset output directory.
          For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point.
          *Cannot be used with multiple entryPoints or together with ``outdir``.*
        - ``buildOptions.absWorkingDir: string``
          Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_.
          If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).

        :see: https://esbuild.github.io/api/#build-api
        '''
        result = self._values.get("build_options")
        return typing.cast(typing.Optional[BuildOptions], result)

    @builtins.property
    def build_provider(self) -> typing.Optional[IBuildProvider]:
        '''The esbuild Build API implementation to be used.

        Configure the default ``EsbuildProvider`` for more options or
        provide a custom ``IBuildProvider`` as an escape hatch.

        :default: new EsbuildProvider()
        '''
        result = self._values.get("build_provider")
        return typing.cast(typing.Optional[IBuildProvider], result)

    @builtins.property
    def copy_dir(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]]:
        '''Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs.

        - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory.
        - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied.

        Therefore the following values for ``copyDir`` are all equivalent::

           { copyDir: "path/to/source" }
           { copyDir: ["path/to/source"] }
           { copyDir: { ".": "path/to/source" } }
           { copyDir: { ".": ["path/to/source"] } }

        The destination cannot be outside of the asset staging directory.
        If you are receiving the error "Cannot copy files to outside of the asset staging directory."
        you are likely using ``..`` or an absolute path as key on the ``copyDir`` map.
        Instead use only relative paths and avoid ``..``.
        '''
        result = self._values.get("copy_dir")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''A hash of this asset, which is available at construction time.

        As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed.

        Defaults to a hash of all files in the resulting bundle.
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TypeScriptSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.AssetProps",
    jsii_struct_bases=[BundlerProps],
    name_mapping={
        "build_options": "buildOptions",
        "build_provider": "buildProvider",
        "copy_dir": "copyDir",
        "entry_points": "entryPoints",
        "asset_hash": "assetHash",
    },
)
class AssetProps(BundlerProps):
    def __init__(
        self,
        *,
        build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_provider: typing.Optional[IBuildProvider] = None,
        copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
        entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
        asset_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_options: Build options passed on to esbuild. Please refer to the esbuild Build API docs for details. - ``buildOptions.outdir: string`` The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory. For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory. *Cannot be used together with ``outfile``*. - ``buildOptions.outfile: string`` Relative path to a file inside the CDK asset output directory. For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point. *Cannot be used with multiple entryPoints or together with ``outdir``.* - ``buildOptions.absWorkingDir: string`` Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_. If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).
        :param build_provider: The esbuild Build API implementation to be used. Configure the default ``EsbuildProvider`` for more options or provide a custom ``IBuildProvider`` as an escape hatch. Default: new EsbuildProvider()
        :param copy_dir: Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs. - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory. - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied. Therefore the following values for ``copyDir`` are all equivalent:: { copyDir: "path/to/source" } { copyDir: ["path/to/source"] } { copyDir: { ".": "path/to/source" } } { copyDir: { ".": ["path/to/source"] } } The destination cannot be outside of the asset staging directory. If you are receiving the error "Cannot copy files to outside of the asset staging directory." you are likely using ``..`` or an absolute path as key on the ``copyDir`` map. Instead use only relative paths and avoid ``..``.
        :param entry_points: A path or list or map of paths to the entry points of your code. Relative paths are by default resolved from the current working directory. To change the working directory, see ``buildOptions.absWorkingDir``. Absolute paths can be used if files are part of the working directory. Examples: - ``'src/index.ts'`` - ``require.resolve('./lambda')`` - ``['src/index.ts', 'src/util.ts']`` - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        :param asset_hash: A hash of this asset, which is available at construction time. As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed. Defaults to a hash of all files in the resulting bundle.
        '''
        if isinstance(build_options, dict):
            build_options = BuildOptions(**build_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7937333d15fe5f9ba92829f137d9a036851e736b6e308a22c1a87c90ba239d3)
            check_type(argname="argument build_options", value=build_options, expected_type=type_hints["build_options"])
            check_type(argname="argument build_provider", value=build_provider, expected_type=type_hints["build_provider"])
            check_type(argname="argument copy_dir", value=copy_dir, expected_type=type_hints["copy_dir"])
            check_type(argname="argument entry_points", value=entry_points, expected_type=type_hints["entry_points"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entry_points": entry_points,
        }
        if build_options is not None:
            self._values["build_options"] = build_options
        if build_provider is not None:
            self._values["build_provider"] = build_provider
        if copy_dir is not None:
            self._values["copy_dir"] = copy_dir
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash

    @builtins.property
    def build_options(self) -> typing.Optional[BuildOptions]:
        '''Build options passed on to esbuild. Please refer to the esbuild Build API docs for details.

        - ``buildOptions.outdir: string``
          The actual path for the output directory is defined by CDK. However setting this option allows to write files into a subdirectory.
          For example ``{ outdir: 'js' }`` will create an asset with a single directory called ``js``, which contains all built files. This approach can be useful for static website deployments, where JavaScript code should be placed into a subdirectory.
          *Cannot be used together with ``outfile``*.
        - ``buildOptions.outfile: string``
          Relative path to a file inside the CDK asset output directory.
          For example ``{ outfile: 'js/index.js' }`` will create an asset with a single directory called ``js``, which contains a single file ``index.js``. This can be useful to rename the entry point.
          *Cannot be used with multiple entryPoints or together with ``outdir``.*
        - ``buildOptions.absWorkingDir: string``
          Absolute path to the `esbuild working directory <https://esbuild.github.io/api/#working-directory>`_ and defaults to the `current working directory <https://en.wikipedia.org/wiki/Working_directory>`_.
          If paths cannot be found, a good starting point is to look at the concatenation of ``absWorkingDir + entryPoint``. It must always be a valid absolute path pointing to the entry point. When needed, the probably easiest way to set absWorkingDir is to use a combination of ``resolve`` and ``__dirname`` (see "Library authors" section in the documentation).

        :see: https://esbuild.github.io/api/#build-api
        '''
        result = self._values.get("build_options")
        return typing.cast(typing.Optional[BuildOptions], result)

    @builtins.property
    def build_provider(self) -> typing.Optional[IBuildProvider]:
        '''The esbuild Build API implementation to be used.

        Configure the default ``EsbuildProvider`` for more options or
        provide a custom ``IBuildProvider`` as an escape hatch.

        :default: new EsbuildProvider()
        '''
        result = self._values.get("build_provider")
        return typing.cast(typing.Optional[IBuildProvider], result)

    @builtins.property
    def copy_dir(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]]:
        '''Copy additional files to the code `asset staging directory <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.AssetStaging.html#absolutestagedpath>`_, before the build runs. Files copied like this will be overwritten by esbuild if they share the same name as any of the outputs.

        - When provided with a ``string`` or ``array``, all files are copied to the root of asset staging directory.
        - When given a ``map``, the key indicates the destination relative to the asset staging directory and the value is a list of all sources to be copied.

        Therefore the following values for ``copyDir`` are all equivalent::

           { copyDir: "path/to/source" }
           { copyDir: ["path/to/source"] }
           { copyDir: { ".": "path/to/source" } }
           { copyDir: { ".": ["path/to/source"] } }

        The destination cannot be outside of the asset staging directory.
        If you are receiving the error "Cannot copy files to outside of the asset staging directory."
        you are likely using ``..`` or an absolute path as key on the ``copyDir`` map.
        Instead use only relative paths and avoid ``..``.
        '''
        result = self._values.get("copy_dir")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]], result)

    @builtins.property
    def entry_points(
        self,
    ) -> typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]]:
        '''A path or list or map of paths to the entry points of your code.

        Relative paths are by default resolved from the current working directory.
        To change the working directory, see ``buildOptions.absWorkingDir``.

        Absolute paths can be used if files are part of the working directory.

        Examples:

        - ``'src/index.ts'``
        - ``require.resolve('./lambda')``
        - ``['src/index.ts', 'src/util.ts']``
        - ``{one: 'src/two.ts', two: 'src/one.ts'}``
        '''
        result = self._values.get("entry_points")
        assert result is not None, "Required property 'entry_points' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str], typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''A hash of this asset, which is available at construction time.

        As this is a plain string, it can be used in construct IDs in order to enforce creation of a new resource when the content hash has changed.

        Defaults to a hash of all files in the resulting bundle.
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IBuildProvider, ITransformProvider)
class EsbuildProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@mrgrain/cdk-esbuild.EsbuildProvider",
):
    '''Default esbuild implementation calling esbuild's JavaScript API.'''

    def __init__(
        self,
        *,
        esbuild_binary_path: typing.Optional[builtins.str] = None,
        esbuild_module_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param esbuild_binary_path: Path to the binary used by esbuild. This is the same as setting the ESBUILD_BINARY_PATH environment variable.
        :param esbuild_module_path: Absolute path to the esbuild module JS file. E.g. "/home/user/.npm/node_modules/esbuild/lib/main.js" If not set, the module path will be determined in the following order: - Use a path from the ``CDK_ESBUILD_MODULE_PATH`` environment variable - In TypeScript, fallback to the default Node.js package resolution mechanism - All other languages (Python, Go, .NET, Java) use an automatic "best effort" resolution mechanism. The exact algorithm of this mechanism is considered an implementation detail and should not be relied on. If ``esbuild`` cannot be found, it might be installed dynamically to a temporary location. To opt-out of this behavior, set either ``esbuildModulePath`` or ``CDK_ESBUILD_MODULE_PATH`` env variable. Use the static methods on ``EsbuildSource`` to customize the default behavior. Default: - ``CDK_ESBUILD_MODULE_PATH`` or package resolution (see description)
        '''
        props = EsbuildProviderProps(
            esbuild_binary_path=esbuild_binary_path,
            esbuild_module_path=esbuild_module_path,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="defaultBuildProvider")
    @builtins.classmethod
    def default_build_provider(cls) -> IBuildProvider:
        '''Get the default implementation for the Build API.'''
        return typing.cast(IBuildProvider, jsii.sinvoke(cls, "defaultBuildProvider", []))

    @jsii.member(jsii_name="defaultTransformationProvider")
    @builtins.classmethod
    def default_transformation_provider(cls) -> ITransformProvider:
        '''Get the default implementation for the Transformation API.'''
        return typing.cast(ITransformProvider, jsii.sinvoke(cls, "defaultTransformationProvider", []))

    @jsii.member(jsii_name="overrideDefaultBuildProvider")
    @builtins.classmethod
    def override_default_build_provider(cls, provider: IBuildProvider) -> None:
        '''Set the default implementation for the Build API.

        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce55185c1f4e4ea2543ffc50435b6955a1975699390882a132ab05a4b1059224)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(None, jsii.sinvoke(cls, "overrideDefaultBuildProvider", [provider]))

    @jsii.member(jsii_name="overrideDefaultProvider")
    @builtins.classmethod
    def override_default_provider(cls, provider: "IEsbuildProvider") -> None:
        '''Set the default implementation for both Build and Transformation API.

        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c303647ac911205ca4b4cd7077e2f2e5a65d8839915efc836932fb59a119ad)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(None, jsii.sinvoke(cls, "overrideDefaultProvider", [provider]))

    @jsii.member(jsii_name="overrideDefaultTransformationProvider")
    @builtins.classmethod
    def override_default_transformation_provider(
        cls,
        provider: ITransformProvider,
    ) -> None:
        '''Set the default implementation for the Transformation API.

        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710b9d42ec026dfbd46b282d4ed1c516e0e87c1abf5aa4e5d3c6f5fe41872c32)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(None, jsii.sinvoke(cls, "overrideDefaultTransformationProvider", [provider]))

    @jsii.member(jsii_name="buildSync")
    def build_sync(
        self,
        *,
        entry_points: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]]] = None,
        abs_working_dir: typing.Optional[builtins.str] = None,
        alias: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allow_overwrite: typing.Optional[builtins.bool] = None,
        asset_names: typing.Optional[builtins.str] = None,
        banner: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bundle: typing.Optional[builtins.bool] = None,
        charset: typing.Optional[builtins.str] = None,
        chunk_names: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        entry_names: typing.Optional[builtins.str] = None,
        external: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        inject: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        metafile: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        node_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbase: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        out_extension: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outfile: typing.Optional[builtins.str] = None,
        packages: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        preserve_symlinks: typing.Optional[builtins.bool] = None,
        public_path: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        resolve_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        splitting: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig: typing.Optional[builtins.str] = None,
        write: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''A method implementing the code build.

        During synth time, the method will receive all computed ``BuildOptions`` from the bundler.

        It MUST implement any output options to integrate correctly and MAY use any other options.
        On failure, it SHOULD print any warnings & errors to stderr and throw a ``BuildFailure`` to inform the bundler.

        :param entry_points: Documentation: https://esbuild.github.io/api/#entry-points.
        :param abs_working_dir: Documentation: https://esbuild.github.io/api/#working-directory.
        :param alias: Documentation: https://esbuild.github.io/api/#alias.
        :param allow_overwrite: Documentation: https://esbuild.github.io/api/#allow-overwrite.
        :param asset_names: Documentation: https://esbuild.github.io/api/#asset-names.
        :param banner: Documentation: https://esbuild.github.io/api/#banner.
        :param bundle: Documentation: https://esbuild.github.io/api/#bundle.
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param chunk_names: Documentation: https://esbuild.github.io/api/#chunk-names.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param conditions: Documentation: https://esbuild.github.io/api/#conditions.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param entry_names: Documentation: https://esbuild.github.io/api/#entry-names.
        :param external: Documentation: https://esbuild.github.io/api/#external.
        :param footer: Documentation: https://esbuild.github.io/api/#footer.
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param inject: Documentation: https://esbuild.github.io/api/#inject.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: Documentation: https://esbuild.github.io/api/#loader.
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param main_fields: Documentation: https://esbuild.github.io/api/#main-fields.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param metafile: Documentation: https://esbuild.github.io/api/#metafile.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param node_paths: Documentation: https://esbuild.github.io/api/#node-paths.
        :param outbase: Documentation: https://esbuild.github.io/api/#outbase.
        :param outdir: Documentation: https://esbuild.github.io/api/#outdir.
        :param out_extension: Documentation: https://esbuild.github.io/api/#out-extension.
        :param outfile: Documentation: https://esbuild.github.io/api/#outfile.
        :param packages: Documentation: https://esbuild.github.io/api/#packages.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param preserve_symlinks: Documentation: https://esbuild.github.io/api/#preserve-symlinks.
        :param public_path: Documentation: https://esbuild.github.io/api/#public-path.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param resolve_extensions: Documentation: https://esbuild.github.io/api/#resolve-extensions.
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param splitting: Documentation: https://esbuild.github.io/api/#splitting.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig: Documentation: https://esbuild.github.io/api/#tsconfig.
        :param write: Documentation: https://esbuild.github.io/api/#write.
        '''
        options = ProviderBuildOptions(
            entry_points=entry_points,
            abs_working_dir=abs_working_dir,
            alias=alias,
            allow_overwrite=allow_overwrite,
            asset_names=asset_names,
            banner=banner,
            bundle=bundle,
            charset=charset,
            chunk_names=chunk_names,
            color=color,
            conditions=conditions,
            define=define,
            drop=drop,
            entry_names=entry_names,
            external=external,
            footer=footer,
            format=format,
            global_name=global_name,
            ignore_annotations=ignore_annotations,
            inject=inject,
            jsx=jsx,
            jsx_dev=jsx_dev,
            jsx_factory=jsx_factory,
            jsx_fragment=jsx_fragment,
            jsx_import_source=jsx_import_source,
            jsx_side_effects=jsx_side_effects,
            keep_names=keep_names,
            legal_comments=legal_comments,
            loader=loader,
            log_level=log_level,
            log_limit=log_limit,
            log_override=log_override,
            main_fields=main_fields,
            mangle_cache=mangle_cache,
            mangle_props=mangle_props,
            mangle_quoted=mangle_quoted,
            metafile=metafile,
            minify=minify,
            minify_identifiers=minify_identifiers,
            minify_syntax=minify_syntax,
            minify_whitespace=minify_whitespace,
            node_paths=node_paths,
            outbase=outbase,
            outdir=outdir,
            out_extension=out_extension,
            outfile=outfile,
            packages=packages,
            platform=platform,
            preserve_symlinks=preserve_symlinks,
            public_path=public_path,
            pure=pure,
            reserve_props=reserve_props,
            resolve_extensions=resolve_extensions,
            sourcemap=sourcemap,
            source_root=source_root,
            sources_content=sources_content,
            splitting=splitting,
            supported=supported,
            target=target,
            tree_shaking=tree_shaking,
            tsconfig=tsconfig,
            write=write,
        )

        return typing.cast(None, jsii.invoke(self, "buildSync", [options]))

    @jsii.member(jsii_name="transformSync")
    def transform_sync(
        self,
        input: builtins.str,
        *,
        banner: typing.Optional[builtins.str] = None,
        charset: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        platform: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        sourcefile: typing.Optional[builtins.str] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union[TsconfigOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> builtins.str:
        '''A method implementing the inline code transformation.

        During synth time, the method will receive the inline code and all computed ``TransformOptions`` from the bundler.

        MUST return the transformed code as a string to integrate correctly.
        It MAY use these options to do so.
        On failure, it SHOULD print any warnings & errors to stderr and throw a ``TransformFailure`` to inform the bundler.

        :param input: -
        :param banner: 
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param footer: 
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: 
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param sourcefile: 
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig_raw: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4518845e9c0cd47623e425def75422413186f9fae8d2e5056f61f917f5d888e4)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
        options = ProviderTransformOptions(
            banner=banner,
            charset=charset,
            color=color,
            define=define,
            drop=drop,
            footer=footer,
            format=format,
            global_name=global_name,
            ignore_annotations=ignore_annotations,
            jsx=jsx,
            jsx_dev=jsx_dev,
            jsx_factory=jsx_factory,
            jsx_fragment=jsx_fragment,
            jsx_import_source=jsx_import_source,
            jsx_side_effects=jsx_side_effects,
            keep_names=keep_names,
            legal_comments=legal_comments,
            loader=loader,
            log_level=log_level,
            log_limit=log_limit,
            log_override=log_override,
            mangle_cache=mangle_cache,
            mangle_props=mangle_props,
            mangle_quoted=mangle_quoted,
            minify=minify,
            minify_identifiers=minify_identifiers,
            minify_syntax=minify_syntax,
            minify_whitespace=minify_whitespace,
            platform=platform,
            pure=pure,
            reserve_props=reserve_props,
            sourcefile=sourcefile,
            sourcemap=sourcemap,
            source_root=source_root,
            sources_content=sources_content,
            supported=supported,
            target=target,
            tree_shaking=tree_shaking,
            tsconfig_raw=tsconfig_raw,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "transformSync", [input, options]))


@jsii.interface(jsii_type="@mrgrain/cdk-esbuild.IEsbuildProvider")
class IEsbuildProvider(IBuildProvider, ITransformProvider, typing_extensions.Protocol):
    '''Provides an implementation of the esbuild Build & Transform API.'''

    pass


class _IEsbuildProviderProxy(
    jsii.proxy_for(IBuildProvider), # type: ignore[misc]
    jsii.proxy_for(ITransformProvider), # type: ignore[misc]
):
    '''Provides an implementation of the esbuild Build & Transform API.'''

    __jsii_type__: typing.ClassVar[str] = "@mrgrain/cdk-esbuild.IEsbuildProvider"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEsbuildProvider).__jsii_proxy_class__ = lambda : _IEsbuildProviderProxy


@jsii.data_type(
    jsii_type="@mrgrain/cdk-esbuild.ProviderTransformOptions",
    jsii_struct_bases=[TransformOptions],
    name_mapping={
        "banner": "banner",
        "charset": "charset",
        "color": "color",
        "define": "define",
        "drop": "drop",
        "footer": "footer",
        "format": "format",
        "global_name": "globalName",
        "ignore_annotations": "ignoreAnnotations",
        "jsx": "jsx",
        "jsx_dev": "jsxDev",
        "jsx_factory": "jsxFactory",
        "jsx_fragment": "jsxFragment",
        "jsx_import_source": "jsxImportSource",
        "jsx_side_effects": "jsxSideEffects",
        "keep_names": "keepNames",
        "legal_comments": "legalComments",
        "loader": "loader",
        "log_level": "logLevel",
        "log_limit": "logLimit",
        "log_override": "logOverride",
        "mangle_cache": "mangleCache",
        "mangle_props": "mangleProps",
        "mangle_quoted": "mangleQuoted",
        "minify": "minify",
        "minify_identifiers": "minifyIdentifiers",
        "minify_syntax": "minifySyntax",
        "minify_whitespace": "minifyWhitespace",
        "platform": "platform",
        "pure": "pure",
        "reserve_props": "reserveProps",
        "sourcefile": "sourcefile",
        "sourcemap": "sourcemap",
        "source_root": "sourceRoot",
        "sources_content": "sourcesContent",
        "supported": "supported",
        "target": "target",
        "tree_shaking": "treeShaking",
        "tsconfig_raw": "tsconfigRaw",
    },
)
class ProviderTransformOptions(TransformOptions):
    def __init__(
        self,
        *,
        banner: typing.Optional[builtins.str] = None,
        charset: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        global_name: typing.Optional[builtins.str] = None,
        ignore_annotations: typing.Optional[builtins.bool] = None,
        jsx: typing.Optional[builtins.str] = None,
        jsx_dev: typing.Optional[builtins.bool] = None,
        jsx_factory: typing.Optional[builtins.str] = None,
        jsx_fragment: typing.Optional[builtins.str] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        jsx_side_effects: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        legal_comments: typing.Optional[builtins.str] = None,
        loader: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        log_limit: typing.Optional[jsii.Number] = None,
        log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        mangle_props: typing.Any = None,
        mangle_quoted: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        minify_identifiers: typing.Optional[builtins.bool] = None,
        minify_syntax: typing.Optional[builtins.bool] = None,
        minify_whitespace: typing.Optional[builtins.bool] = None,
        platform: typing.Optional[builtins.str] = None,
        pure: typing.Optional[typing.Sequence[builtins.str]] = None,
        reserve_props: typing.Any = None,
        sourcefile: typing.Optional[builtins.str] = None,
        sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        source_root: typing.Optional[builtins.str] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        tree_shaking: typing.Optional[builtins.bool] = None,
        tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union[TsconfigOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param banner: 
        :param charset: Documentation: https://esbuild.github.io/api/#charset.
        :param color: Documentation: https://esbuild.github.io/api/#color.
        :param define: Documentation: https://esbuild.github.io/api/#define.
        :param drop: Documentation: https://esbuild.github.io/api/#drop.
        :param footer: 
        :param format: Documentation: https://esbuild.github.io/api/#format.
        :param global_name: Documentation: https://esbuild.github.io/api/#global-name.
        :param ignore_annotations: Documentation: https://esbuild.github.io/api/#ignore-annotations.
        :param jsx: Documentation: https://esbuild.github.io/api/#jsx.
        :param jsx_dev: Documentation: https://esbuild.github.io/api/#jsx-development.
        :param jsx_factory: Documentation: https://esbuild.github.io/api/#jsx-factory.
        :param jsx_fragment: Documentation: https://esbuild.github.io/api/#jsx-fragment.
        :param jsx_import_source: Documentation: https://esbuild.github.io/api/#jsx-import-source.
        :param jsx_side_effects: Documentation: https://esbuild.github.io/api/#jsx-side-effects.
        :param keep_names: Documentation: https://esbuild.github.io/api/#keep-names.
        :param legal_comments: Documentation: https://esbuild.github.io/api/#legal-comments.
        :param loader: 
        :param log_level: Documentation: https://esbuild.github.io/api/#log-level.
        :param log_limit: Documentation: https://esbuild.github.io/api/#log-limit.
        :param log_override: Documentation: https://esbuild.github.io/api/#log-override.
        :param mangle_cache: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param mangle_quoted: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param minify: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_identifiers: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_syntax: Documentation: https://esbuild.github.io/api/#minify.
        :param minify_whitespace: Documentation: https://esbuild.github.io/api/#minify.
        :param platform: Documentation: https://esbuild.github.io/api/#platform.
        :param pure: Documentation: https://esbuild.github.io/api/#pure.
        :param reserve_props: Documentation: https://esbuild.github.io/api/#mangle-props.
        :param sourcefile: 
        :param sourcemap: Documentation: https://esbuild.github.io/api/#sourcemap.
        :param source_root: Documentation: https://esbuild.github.io/api/#source-root.
        :param sources_content: Documentation: https://esbuild.github.io/api/#sources-content.
        :param supported: Documentation: https://esbuild.github.io/api/#supported.
        :param target: Documentation: https://esbuild.github.io/api/#target.
        :param tree_shaking: Documentation: https://esbuild.github.io/api/#tree-shaking.
        :param tsconfig_raw: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884b5e431e012b418b1076d2d6b7d3430be27ad832de2bbd7bbc2412d2ae6999)
            check_type(argname="argument banner", value=banner, expected_type=type_hints["banner"])
            check_type(argname="argument charset", value=charset, expected_type=type_hints["charset"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument define", value=define, expected_type=type_hints["define"])
            check_type(argname="argument drop", value=drop, expected_type=type_hints["drop"])
            check_type(argname="argument footer", value=footer, expected_type=type_hints["footer"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument global_name", value=global_name, expected_type=type_hints["global_name"])
            check_type(argname="argument ignore_annotations", value=ignore_annotations, expected_type=type_hints["ignore_annotations"])
            check_type(argname="argument jsx", value=jsx, expected_type=type_hints["jsx"])
            check_type(argname="argument jsx_dev", value=jsx_dev, expected_type=type_hints["jsx_dev"])
            check_type(argname="argument jsx_factory", value=jsx_factory, expected_type=type_hints["jsx_factory"])
            check_type(argname="argument jsx_fragment", value=jsx_fragment, expected_type=type_hints["jsx_fragment"])
            check_type(argname="argument jsx_import_source", value=jsx_import_source, expected_type=type_hints["jsx_import_source"])
            check_type(argname="argument jsx_side_effects", value=jsx_side_effects, expected_type=type_hints["jsx_side_effects"])
            check_type(argname="argument keep_names", value=keep_names, expected_type=type_hints["keep_names"])
            check_type(argname="argument legal_comments", value=legal_comments, expected_type=type_hints["legal_comments"])
            check_type(argname="argument loader", value=loader, expected_type=type_hints["loader"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument log_limit", value=log_limit, expected_type=type_hints["log_limit"])
            check_type(argname="argument log_override", value=log_override, expected_type=type_hints["log_override"])
            check_type(argname="argument mangle_cache", value=mangle_cache, expected_type=type_hints["mangle_cache"])
            check_type(argname="argument mangle_props", value=mangle_props, expected_type=type_hints["mangle_props"])
            check_type(argname="argument mangle_quoted", value=mangle_quoted, expected_type=type_hints["mangle_quoted"])
            check_type(argname="argument minify", value=minify, expected_type=type_hints["minify"])
            check_type(argname="argument minify_identifiers", value=minify_identifiers, expected_type=type_hints["minify_identifiers"])
            check_type(argname="argument minify_syntax", value=minify_syntax, expected_type=type_hints["minify_syntax"])
            check_type(argname="argument minify_whitespace", value=minify_whitespace, expected_type=type_hints["minify_whitespace"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument pure", value=pure, expected_type=type_hints["pure"])
            check_type(argname="argument reserve_props", value=reserve_props, expected_type=type_hints["reserve_props"])
            check_type(argname="argument sourcefile", value=sourcefile, expected_type=type_hints["sourcefile"])
            check_type(argname="argument sourcemap", value=sourcemap, expected_type=type_hints["sourcemap"])
            check_type(argname="argument source_root", value=source_root, expected_type=type_hints["source_root"])
            check_type(argname="argument sources_content", value=sources_content, expected_type=type_hints["sources_content"])
            check_type(argname="argument supported", value=supported, expected_type=type_hints["supported"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument tree_shaking", value=tree_shaking, expected_type=type_hints["tree_shaking"])
            check_type(argname="argument tsconfig_raw", value=tsconfig_raw, expected_type=type_hints["tsconfig_raw"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if banner is not None:
            self._values["banner"] = banner
        if charset is not None:
            self._values["charset"] = charset
        if color is not None:
            self._values["color"] = color
        if define is not None:
            self._values["define"] = define
        if drop is not None:
            self._values["drop"] = drop
        if footer is not None:
            self._values["footer"] = footer
        if format is not None:
            self._values["format"] = format
        if global_name is not None:
            self._values["global_name"] = global_name
        if ignore_annotations is not None:
            self._values["ignore_annotations"] = ignore_annotations
        if jsx is not None:
            self._values["jsx"] = jsx
        if jsx_dev is not None:
            self._values["jsx_dev"] = jsx_dev
        if jsx_factory is not None:
            self._values["jsx_factory"] = jsx_factory
        if jsx_fragment is not None:
            self._values["jsx_fragment"] = jsx_fragment
        if jsx_import_source is not None:
            self._values["jsx_import_source"] = jsx_import_source
        if jsx_side_effects is not None:
            self._values["jsx_side_effects"] = jsx_side_effects
        if keep_names is not None:
            self._values["keep_names"] = keep_names
        if legal_comments is not None:
            self._values["legal_comments"] = legal_comments
        if loader is not None:
            self._values["loader"] = loader
        if log_level is not None:
            self._values["log_level"] = log_level
        if log_limit is not None:
            self._values["log_limit"] = log_limit
        if log_override is not None:
            self._values["log_override"] = log_override
        if mangle_cache is not None:
            self._values["mangle_cache"] = mangle_cache
        if mangle_props is not None:
            self._values["mangle_props"] = mangle_props
        if mangle_quoted is not None:
            self._values["mangle_quoted"] = mangle_quoted
        if minify is not None:
            self._values["minify"] = minify
        if minify_identifiers is not None:
            self._values["minify_identifiers"] = minify_identifiers
        if minify_syntax is not None:
            self._values["minify_syntax"] = minify_syntax
        if minify_whitespace is not None:
            self._values["minify_whitespace"] = minify_whitespace
        if platform is not None:
            self._values["platform"] = platform
        if pure is not None:
            self._values["pure"] = pure
        if reserve_props is not None:
            self._values["reserve_props"] = reserve_props
        if sourcefile is not None:
            self._values["sourcefile"] = sourcefile
        if sourcemap is not None:
            self._values["sourcemap"] = sourcemap
        if source_root is not None:
            self._values["source_root"] = source_root
        if sources_content is not None:
            self._values["sources_content"] = sources_content
        if supported is not None:
            self._values["supported"] = supported
        if target is not None:
            self._values["target"] = target
        if tree_shaking is not None:
            self._values["tree_shaking"] = tree_shaking
        if tsconfig_raw is not None:
            self._values["tsconfig_raw"] = tsconfig_raw

    @builtins.property
    def banner(self) -> typing.Optional[builtins.str]:
        result = self._values.get("banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def charset(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#charset.'''
        result = self._values.get("charset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#color.'''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def define(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#define.'''
        result = self._values.get("define")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def drop(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#drop.'''
        result = self._values.get("drop")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def footer(self) -> typing.Optional[builtins.str]:
        result = self._values.get("footer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#format.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_name(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#global-name.'''
        result = self._values.get("global_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_annotations(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#ignore-annotations.'''
        result = self._values.get("ignore_annotations")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx.'''
        result = self._values.get("jsx")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_dev(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-development.'''
        result = self._values.get("jsx_dev")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx_factory(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-factory.'''
        result = self._values.get("jsx_factory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_fragment(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-fragment.'''
        result = self._values.get("jsx_fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_import_source(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#jsx-import-source.'''
        result = self._values.get("jsx_import_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsx_side_effects(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#jsx-side-effects.'''
        result = self._values.get("jsx_side_effects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def keep_names(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#keep-names.'''
        result = self._values.get("keep_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def legal_comments(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#legal-comments.'''
        result = self._values.get("legal_comments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def loader(self) -> typing.Optional[builtins.str]:
        result = self._values.get("loader")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#log-level.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_limit(self) -> typing.Optional[jsii.Number]:
        '''Documentation: https://esbuild.github.io/api/#log-limit.'''
        result = self._values.get("log_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_override(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#log-override.'''
        result = self._values.get("log_override")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mangle_cache(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_cache")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]], result)

    @builtins.property
    def mangle_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def mangle_quoted(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("mangle_quoted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_identifiers(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_identifiers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_syntax(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_syntax")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify_whitespace(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#minify.'''
        result = self._values.get("minify_whitespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#platform.'''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pure(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#pure.'''
        result = self._values.get("pure")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reserve_props(self) -> typing.Any:
        '''Documentation: https://esbuild.github.io/api/#mangle-props.'''
        result = self._values.get("reserve_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def sourcefile(self) -> typing.Optional[builtins.str]:
        result = self._values.get("sourcefile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sourcemap(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''Documentation: https://esbuild.github.io/api/#sourcemap.'''
        result = self._values.get("sourcemap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], result)

    @builtins.property
    def source_root(self) -> typing.Optional[builtins.str]:
        '''Documentation: https://esbuild.github.io/api/#source-root.'''
        result = self._values.get("source_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources_content(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#sources-content.'''
        result = self._values.get("sources_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supported(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.bool]]:
        '''Documentation: https://esbuild.github.io/api/#supported.'''
        result = self._values.get("supported")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.bool]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''Documentation: https://esbuild.github.io/api/#target.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def tree_shaking(self) -> typing.Optional[builtins.bool]:
        '''Documentation: https://esbuild.github.io/api/#tree-shaking.'''
        result = self._values.get("tree_shaking")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tsconfig_raw(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, TsconfigOptions]]:
        result = self._values.get("tsconfig_raw")
        return typing.cast(typing.Optional[typing.Union[builtins.str, TsconfigOptions]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderTransformOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AssetProps",
    "BuildOptions",
    "BundlerProps",
    "CodeConfig",
    "CompilerOptions",
    "EsbuildAsset",
    "EsbuildBundler",
    "EsbuildCode",
    "EsbuildProvider",
    "EsbuildProviderProps",
    "EsbuildSource",
    "IBuildProvider",
    "IEsbuildProvider",
    "ITransformProvider",
    "InlineJavaScriptCode",
    "InlineTypeScriptCode",
    "JavaScriptAsset",
    "JavaScriptCode",
    "JavaScriptCodeProps",
    "JavaScriptSource",
    "JavaScriptSourceProps",
    "ProviderBuildOptions",
    "ProviderTransformOptions",
    "TransformOptions",
    "TransformerProps",
    "TsconfigOptions",
    "TypeScriptAsset",
    "TypeScriptCode",
    "TypeScriptCodeProps",
    "TypeScriptSource",
    "TypeScriptSourceProps",
]

publication.publish()

def _typecheckingstub__cf3dbfe8b02ff3b7a13b707799738cc16cd402c4e3086f60eb8f86814c6b2680(
    *,
    abs_working_dir: typing.Optional[builtins.str] = None,
    alias: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    allow_overwrite: typing.Optional[builtins.bool] = None,
    asset_names: typing.Optional[builtins.str] = None,
    banner: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bundle: typing.Optional[builtins.bool] = None,
    charset: typing.Optional[builtins.str] = None,
    chunk_names: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    entry_names: typing.Optional[builtins.str] = None,
    external: typing.Optional[typing.Sequence[builtins.str]] = None,
    footer: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    format: typing.Optional[builtins.str] = None,
    global_name: typing.Optional[builtins.str] = None,
    ignore_annotations: typing.Optional[builtins.bool] = None,
    inject: typing.Optional[typing.Sequence[builtins.str]] = None,
    jsx: typing.Optional[builtins.str] = None,
    jsx_dev: typing.Optional[builtins.bool] = None,
    jsx_factory: typing.Optional[builtins.str] = None,
    jsx_fragment: typing.Optional[builtins.str] = None,
    jsx_import_source: typing.Optional[builtins.str] = None,
    jsx_side_effects: typing.Optional[builtins.bool] = None,
    keep_names: typing.Optional[builtins.bool] = None,
    legal_comments: typing.Optional[builtins.str] = None,
    loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_level: typing.Optional[builtins.str] = None,
    log_limit: typing.Optional[jsii.Number] = None,
    log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    mangle_props: typing.Any = None,
    mangle_quoted: typing.Optional[builtins.bool] = None,
    metafile: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    minify_identifiers: typing.Optional[builtins.bool] = None,
    minify_syntax: typing.Optional[builtins.bool] = None,
    minify_whitespace: typing.Optional[builtins.bool] = None,
    node_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    outbase: typing.Optional[builtins.str] = None,
    outdir: typing.Optional[builtins.str] = None,
    out_extension: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    outfile: typing.Optional[builtins.str] = None,
    packages: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    preserve_symlinks: typing.Optional[builtins.bool] = None,
    public_path: typing.Optional[builtins.str] = None,
    pure: typing.Optional[typing.Sequence[builtins.str]] = None,
    reserve_props: typing.Any = None,
    resolve_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    source_root: typing.Optional[builtins.str] = None,
    sources_content: typing.Optional[builtins.bool] = None,
    splitting: typing.Optional[builtins.bool] = None,
    supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
    target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    tree_shaking: typing.Optional[builtins.bool] = None,
    tsconfig: typing.Optional[builtins.str] = None,
    write: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9873d08db3203496e0d96907173153080076971ae0098d003ebff0ccaffdb97(
    *,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c185489c0b0ad068a8687186a8aaa4be606d632824af7246f2c55827feaacf(
    *,
    image: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.CodeImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inline_code: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.Location, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b682d31bc71983a448565f5ef0a021abb3aeaf127a6dab66c921bef47f98592(
    *,
    imports_not_used_as_values: typing.Optional[builtins.str] = None,
    jsx_factory: typing.Optional[builtins.str] = None,
    jsx_fragment_factory: typing.Optional[builtins.str] = None,
    preserve_value_imports: typing.Optional[builtins.bool] = None,
    use_define_for_class_fields: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ececb4940ec6eae1c73365c13ad8bd754b062cb59e54a4e520ed5b39927f70(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    asset_hash: typing.Optional[builtins.str] = None,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3093569ed2b9b16c3c9014d1d3b5429adba0bf4de17908bc72728a57bb554c84(
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    *,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240365991669493923be1f0bfe12c1cc48bb10fe4c8a3111ab380790be41ccdb(
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    props: typing.Union[typing.Union[JavaScriptCodeProps, typing.Dict[builtins.str, typing.Any]], typing.Union[TypeScriptCodeProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b721a6ee79f34aa33e63b2e59198a8a9838b1b0a4f6f2dda376f64ac2fd3289(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f91f1d460a1f2d5cc64a5396f606c04ca6addf6527dd68a11a6d06d10158a64(
    resource: _aws_cdk_ceddda9d.CfnResource,
    *,
    resource_property: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37de67b53e05897576c1062e32e3fe6075755b5a74e738ef4d3be53583e2153a(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d305fae366aedae68d382d67dcb5b325fddf4dd255defe51b88d29cf64ba09(
    value: EsbuildAsset,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dae3d5ed0d2c7458d21f336873b06a83119c1d01c6e4efdf3f4f083d5fc0c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfd6f14403c8fe61b069ea91e6f7e824c9809aadbf0334c47d49474d2095e95(
    value: AssetProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e2e8be5e24a7fca00969e5b068680339e16f35bbdb62130ad26ff1caaf8318(
    *,
    esbuild_binary_path: typing.Optional[builtins.str] = None,
    esbuild_module_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b273d64922e32225c024bddb7c08e70f30648e2537ff966572dee3fd5267a11d(
    input: builtins.str,
    *,
    banner: typing.Optional[builtins.str] = None,
    charset: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    footer: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    global_name: typing.Optional[builtins.str] = None,
    ignore_annotations: typing.Optional[builtins.bool] = None,
    jsx: typing.Optional[builtins.str] = None,
    jsx_dev: typing.Optional[builtins.bool] = None,
    jsx_factory: typing.Optional[builtins.str] = None,
    jsx_fragment: typing.Optional[builtins.str] = None,
    jsx_import_source: typing.Optional[builtins.str] = None,
    jsx_side_effects: typing.Optional[builtins.bool] = None,
    keep_names: typing.Optional[builtins.bool] = None,
    legal_comments: typing.Optional[builtins.str] = None,
    loader: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    log_limit: typing.Optional[jsii.Number] = None,
    log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    mangle_props: typing.Any = None,
    mangle_quoted: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    minify_identifiers: typing.Optional[builtins.bool] = None,
    minify_syntax: typing.Optional[builtins.bool] = None,
    minify_whitespace: typing.Optional[builtins.bool] = None,
    platform: typing.Optional[builtins.str] = None,
    pure: typing.Optional[typing.Sequence[builtins.str]] = None,
    reserve_props: typing.Any = None,
    sourcefile: typing.Optional[builtins.str] = None,
    sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    source_root: typing.Optional[builtins.str] = None,
    sources_content: typing.Optional[builtins.bool] = None,
    supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
    target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    tree_shaking: typing.Optional[builtins.bool] = None,
    tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union[TsconfigOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc33593af0b89f946131db30a4d4de49eb78d91ea1bef57c8fa9913c4c293dd1(
    code: builtins.str,
    *,
    transform_options: typing.Optional[typing.Union[TransformOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_provider: typing.Optional[ITransformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9288df5c915db457b11d8163428843817b6ab36000054de4834cb9ae4a303c3c(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5bcf0c5b4e074edf1efe7b546b2d926e6c963fbeeebf952ffca5ea0fd7127b(
    code: builtins.str,
    *,
    transform_options: typing.Optional[typing.Union[TransformOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_provider: typing.Optional[ITransformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b8bec45384b1a113e49dc5131a885afb8dd52c5a5dcd74ca0ea30842102152(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7c293653fc1a46e989f4190de1177ebd3f68affe07df2ac666fa2b3e58e333(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    asset_hash: typing.Optional[builtins.str] = None,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4507163c84c56eb03714049d2f473f23bb8125c0f86941f81f35bee2ef4ae03f(
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c44ce71d85c7855ea5a1a555e7ea52d13c85f740db1d0666f73c81fcedac3a(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f39896c298a9022e4c74318bcdd866488de29ae5dbc273a816eaaa87877471(
    *,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    asset_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3f50e082743d1d9113eaf78a36a88b8dc154cac77a4209408270009380d4d0(
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf351b7981d89943eaea281c4e34aa55c78d9b4eb9849cf0bc84d50da8978ed(
    scope: _constructs_77d1e7e8.Construct,
    *,
    handler_role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e925b32744da90e03880eb9891bd0bf67942f59132c9c137e75f4f408ab40b(
    value: typing.Union[JavaScriptAsset, TypeScriptAsset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e346f65f14043eddc497c05af00b110f5b6e76cd9760d9b60e2d4ea8a2fb7c5c(
    value: JavaScriptAsset,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bcb9cb4f34df2e08980b0a37ea87e5c6f31e5450ac3460c110730703dceeba(
    value: AssetProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ef31d1935b5233ddb314ca48b282282a07491a73aaa68ada8337da1d10b4b6(
    *,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    asset_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78e7efccee59986fec35d76ced509c566ac34900b09d44551f2407cbf1cff4b(
    *,
    abs_working_dir: typing.Optional[builtins.str] = None,
    alias: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    allow_overwrite: typing.Optional[builtins.bool] = None,
    asset_names: typing.Optional[builtins.str] = None,
    banner: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bundle: typing.Optional[builtins.bool] = None,
    charset: typing.Optional[builtins.str] = None,
    chunk_names: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    entry_names: typing.Optional[builtins.str] = None,
    external: typing.Optional[typing.Sequence[builtins.str]] = None,
    footer: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    format: typing.Optional[builtins.str] = None,
    global_name: typing.Optional[builtins.str] = None,
    ignore_annotations: typing.Optional[builtins.bool] = None,
    inject: typing.Optional[typing.Sequence[builtins.str]] = None,
    jsx: typing.Optional[builtins.str] = None,
    jsx_dev: typing.Optional[builtins.bool] = None,
    jsx_factory: typing.Optional[builtins.str] = None,
    jsx_fragment: typing.Optional[builtins.str] = None,
    jsx_import_source: typing.Optional[builtins.str] = None,
    jsx_side_effects: typing.Optional[builtins.bool] = None,
    keep_names: typing.Optional[builtins.bool] = None,
    legal_comments: typing.Optional[builtins.str] = None,
    loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_level: typing.Optional[builtins.str] = None,
    log_limit: typing.Optional[jsii.Number] = None,
    log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    mangle_props: typing.Any = None,
    mangle_quoted: typing.Optional[builtins.bool] = None,
    metafile: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    minify_identifiers: typing.Optional[builtins.bool] = None,
    minify_syntax: typing.Optional[builtins.bool] = None,
    minify_whitespace: typing.Optional[builtins.bool] = None,
    node_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    outbase: typing.Optional[builtins.str] = None,
    outdir: typing.Optional[builtins.str] = None,
    out_extension: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    outfile: typing.Optional[builtins.str] = None,
    packages: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    preserve_symlinks: typing.Optional[builtins.bool] = None,
    public_path: typing.Optional[builtins.str] = None,
    pure: typing.Optional[typing.Sequence[builtins.str]] = None,
    reserve_props: typing.Any = None,
    resolve_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    source_root: typing.Optional[builtins.str] = None,
    sources_content: typing.Optional[builtins.bool] = None,
    splitting: typing.Optional[builtins.bool] = None,
    supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
    target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    tree_shaking: typing.Optional[builtins.bool] = None,
    tsconfig: typing.Optional[builtins.str] = None,
    write: typing.Optional[builtins.bool] = None,
    entry_points: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c37248db4a858f2f46ff70ce7ec32f72b189492c09c9e26fc3552cb219fbd47(
    *,
    banner: typing.Optional[builtins.str] = None,
    charset: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    footer: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    global_name: typing.Optional[builtins.str] = None,
    ignore_annotations: typing.Optional[builtins.bool] = None,
    jsx: typing.Optional[builtins.str] = None,
    jsx_dev: typing.Optional[builtins.bool] = None,
    jsx_factory: typing.Optional[builtins.str] = None,
    jsx_fragment: typing.Optional[builtins.str] = None,
    jsx_import_source: typing.Optional[builtins.str] = None,
    jsx_side_effects: typing.Optional[builtins.bool] = None,
    keep_names: typing.Optional[builtins.bool] = None,
    legal_comments: typing.Optional[builtins.str] = None,
    loader: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    log_limit: typing.Optional[jsii.Number] = None,
    log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    mangle_props: typing.Any = None,
    mangle_quoted: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    minify_identifiers: typing.Optional[builtins.bool] = None,
    minify_syntax: typing.Optional[builtins.bool] = None,
    minify_whitespace: typing.Optional[builtins.bool] = None,
    platform: typing.Optional[builtins.str] = None,
    pure: typing.Optional[typing.Sequence[builtins.str]] = None,
    reserve_props: typing.Any = None,
    sourcefile: typing.Optional[builtins.str] = None,
    sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    source_root: typing.Optional[builtins.str] = None,
    sources_content: typing.Optional[builtins.bool] = None,
    supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
    target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    tree_shaking: typing.Optional[builtins.bool] = None,
    tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union[TsconfigOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc58b06985a425c97d91ff68cb5366f217b2e95fc05f434a2c8913993546369b(
    *,
    transform_options: typing.Optional[typing.Union[TransformOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    transform_provider: typing.Optional[ITransformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83734fd122d82939d2ffe79d063580419456cc543d3ed09342815c5d5803d460(
    *,
    compiler_options: typing.Optional[typing.Union[CompilerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4b2df3385e42f976caa97a3cb710e87cff5020eb30f93ab0c57dd209f30e1d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    asset_hash: typing.Optional[builtins.str] = None,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54aaf93a7fa033eebe7abbb99ce48fb8d394e94136697e90200b3c33c8c1e532(
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91527f1d6303f104ddd5d7660026fd21b612b51f01a7fa06355c06e0af22d930(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57f845df99b12169ddd9f6ae8ea59cec6ef4a8067d9c4defe0d44270463afb7(
    *,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    asset_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48105ed0b909a4fdfdc06c3ff865cce3202b96b81ee7be69e7617e62dcf1163(
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbcbde63a5766d4de14a37346c050f53c31a267934171012ccc381663a8036c(
    scope: _constructs_77d1e7e8.Construct,
    *,
    handler_role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a963a15411f9b48fcbd28a99bdfaa2b2f747bad253f6af021f01c0a89d696e(
    value: typing.Union[JavaScriptAsset, TypeScriptAsset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcb1e5a2c95b154e98acdbb52b335f324a32fc76c045c77f7283ad8771105b2(
    value: TypeScriptAsset,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6926cc3b4983633d848a739a5b9e1f74d499f7d5cc41480cac8b0184dade76e7(
    value: AssetProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269edc1e8ae899306e5ef7e6e60a5a9dc94d277d28a0a395bbb0dfd0eaa3e8f7(
    *,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    asset_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7937333d15fe5f9ba92829f137d9a036851e736b6e308a22c1a87c90ba239d3(
    *,
    build_options: typing.Optional[typing.Union[BuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_provider: typing.Optional[IBuildProvider] = None,
    copy_dir: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]]] = None,
    entry_points: typing.Union[builtins.str, typing.Sequence[builtins.str], typing.Mapping[builtins.str, builtins.str]],
    asset_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce55185c1f4e4ea2543ffc50435b6955a1975699390882a132ab05a4b1059224(
    provider: IBuildProvider,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c303647ac911205ca4b4cd7077e2f2e5a65d8839915efc836932fb59a119ad(
    provider: IEsbuildProvider,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710b9d42ec026dfbd46b282d4ed1c516e0e87c1abf5aa4e5d3c6f5fe41872c32(
    provider: ITransformProvider,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4518845e9c0cd47623e425def75422413186f9fae8d2e5056f61f917f5d888e4(
    input: builtins.str,
    *,
    banner: typing.Optional[builtins.str] = None,
    charset: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    footer: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    global_name: typing.Optional[builtins.str] = None,
    ignore_annotations: typing.Optional[builtins.bool] = None,
    jsx: typing.Optional[builtins.str] = None,
    jsx_dev: typing.Optional[builtins.bool] = None,
    jsx_factory: typing.Optional[builtins.str] = None,
    jsx_fragment: typing.Optional[builtins.str] = None,
    jsx_import_source: typing.Optional[builtins.str] = None,
    jsx_side_effects: typing.Optional[builtins.bool] = None,
    keep_names: typing.Optional[builtins.bool] = None,
    legal_comments: typing.Optional[builtins.str] = None,
    loader: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    log_limit: typing.Optional[jsii.Number] = None,
    log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    mangle_props: typing.Any = None,
    mangle_quoted: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    minify_identifiers: typing.Optional[builtins.bool] = None,
    minify_syntax: typing.Optional[builtins.bool] = None,
    minify_whitespace: typing.Optional[builtins.bool] = None,
    platform: typing.Optional[builtins.str] = None,
    pure: typing.Optional[typing.Sequence[builtins.str]] = None,
    reserve_props: typing.Any = None,
    sourcefile: typing.Optional[builtins.str] = None,
    sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    source_root: typing.Optional[builtins.str] = None,
    sources_content: typing.Optional[builtins.bool] = None,
    supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
    target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    tree_shaking: typing.Optional[builtins.bool] = None,
    tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union[TsconfigOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884b5e431e012b418b1076d2d6b7d3430be27ad832de2bbd7bbc2412d2ae6999(
    *,
    banner: typing.Optional[builtins.str] = None,
    charset: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    footer: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    global_name: typing.Optional[builtins.str] = None,
    ignore_annotations: typing.Optional[builtins.bool] = None,
    jsx: typing.Optional[builtins.str] = None,
    jsx_dev: typing.Optional[builtins.bool] = None,
    jsx_factory: typing.Optional[builtins.str] = None,
    jsx_fragment: typing.Optional[builtins.str] = None,
    jsx_import_source: typing.Optional[builtins.str] = None,
    jsx_side_effects: typing.Optional[builtins.bool] = None,
    keep_names: typing.Optional[builtins.bool] = None,
    legal_comments: typing.Optional[builtins.str] = None,
    loader: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    log_limit: typing.Optional[jsii.Number] = None,
    log_override: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mangle_cache: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    mangle_props: typing.Any = None,
    mangle_quoted: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    minify_identifiers: typing.Optional[builtins.bool] = None,
    minify_syntax: typing.Optional[builtins.bool] = None,
    minify_whitespace: typing.Optional[builtins.bool] = None,
    platform: typing.Optional[builtins.str] = None,
    pure: typing.Optional[typing.Sequence[builtins.str]] = None,
    reserve_props: typing.Any = None,
    sourcefile: typing.Optional[builtins.str] = None,
    sourcemap: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    source_root: typing.Optional[builtins.str] = None,
    sources_content: typing.Optional[builtins.bool] = None,
    supported: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
    target: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    tree_shaking: typing.Optional[builtins.bool] = None,
    tsconfig_raw: typing.Optional[typing.Union[builtins.str, typing.Union[TsconfigOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
