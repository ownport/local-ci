# travis2bash

## The Travis CI Build Lifecycle

A build on Travis CI is made up of two steps:

- `install`: install any dependencies required
- `script`: run the build script

You can run custom commands before the installation step (`before_install`), and before (`before_script`) or after (`after_script`) the script step.

In a `before_install` step, you can install additional dependencies required by your project such as Ubuntu packages or custom services.

You can perform additional steps when your build succeeds or fails using the `after_success` (such as building documentation, or deploying to a custom server) or `after_failure` (such as uploading log files) options. In both `after_failure` and `after_success`, you can access the build result using the `$TRAVIS_TEST_RESULT` environment variable.

The complete build lifecycle, including three optional deployment steps and after checking out the git repository and changing to the repository directory, is:

1. Install `apt addons`
2. `before_install`
3. `install`
4. `before_script`
5. `script`
6. `after_success` or `after_failure`
7. OPTIONAL `before_deploy`
8. OPTIONAL `deploy`
9. OPTIONAL `after_deploy`
10. `after_script`

## Skipping the Installation Step

You can skip the installation step entirely by adding the following to your .travis.yml:
```yaml
install: true
```

## Links

- [Travis CI: Customizing the Build](https://docs.travis-ci.com/user/customizing-the-build/)


