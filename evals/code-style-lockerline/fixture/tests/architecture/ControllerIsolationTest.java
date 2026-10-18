package architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

import com.tngtech.archunit.core.importer.ClassFileImporter;
import org.junit.jupiter.api.Test;

class ControllerIsolationTest {
    /**
     * The controller never reaches the courier API; it reports through BankListener (ADR-0001).
     * Checked on the compiled classes, so a call made through reflection is not seen.
     */
    @Test
    void controller_does_not_depend_on_the_courier_api() {
        var classes = new ClassFileImporter().importPackages("lockerline");
        noClasses().that().haveSimpleName("CompartmentController")
            .should().dependOnClassesThat().resideInAPackage("lockerline.courier..")
            .check(classes);
    }
}
